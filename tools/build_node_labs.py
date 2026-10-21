#!/usr/bin/env python3
"""Render one reviewable experiment card per indexed node; never mark it tested."""
import json
import re
from pathlib import Path
from urllib.parse import quote
from lab_cases import CASES

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = json.loads((ROOT/'data/node-schemas.json').read_text())
GROUPS = json.loads((ROOT/'data/experiments.json').read_text())
MEMBERS = {n: g for g in GROUPS for n in g['nodes']}

def case(change, expected, observe):
    return dict(change=change, expected=expected, observe=observe)

def family(n):
    k=n['class_name']; g=MEMBERS[k]['id']; p={i['name']:i for i in n['inputs']}; out={i['type'] for i in n['outputs']}
    setup='先完成所属实验组的上游闭环，保存一份冻结输入；模型文件、dtype、设备与随机种子都记录到实验表。'
    rows=[]; kind='family'
    if 'Loader' in k or k.startswith('Load') and g not in ['A01','C01','C03','A12','C05','G05'] or k=='LoraModelLoader':
        files=[x for x in p if x.endswith(('_name','_file')) or x in ('name','model_path','text_encoder')]
        rows=[case('加载同一份资源两次；文件参数：'+', '.join(files),
              '输出类型/数量应与下表一致，匹配的最小下游任务可运行；第二次可能命中缓存。相同文件在同环境产生相同功能，不能仅以“加载无报错”验收。',
              '记录文件SHA256、返回对象类型、下游输出shape及warm/cold耗时。'),
              case('只将其中一份资源换为同架构兼容的第二文件；若仅有一个资源则恢复同文件重载',
              '实际资源标识必须更新；相同架构的输出接口应保持。输出画面可能变化，不承诺质量方向。没有第二资源则本对照BLOCKED_RESOURCE。',
              '检查日志中的实际加载路径/权重键及下游结果，不同时改type/vae等。')]
        if 'device' in p or 'weight_dtype' in p:
            rows.append(case('只改本机支持的device或weight_dtype之一','设备/精度策略改变；下游shape保持，数值可有精度误差。资源不支持的选项应明确报错，不假定CPU/GPU必然位级一致。','记录实际设备、dtype、耗时和峰值内存；同步完成后计时。'))
    elif k.startswith(('ModelMerge','CLIPMerge')):
        controls=[x for x,i in p.items() if i['type']=='FLOAT']
        setup='准备相同架构、相同参数key/shape的A/B；最好A与B只有一组已知非零权重差，禁止原地覆盖源模型。'
        rows=[case('A与A执行本节点','加法类预期对应权重加倍；减法类在multiplier=1时对应权重为0；插值/分块类A与A应恢复A。按本节点运算分类核对，不能统一判“像原模型”。','读取可合并权重的小样本，不把生成图相似当权重公式证据。'),
              case('仅改变一个权重控制：'+(controls[0] if controls else '将输入B换为已知差分B'),
              '该控制对应参数组的合并系数改变，未选组保持其原系数。对于分块混合，逐组重复0/0.5/1扫描；单组测试不能代替其它组。',
              '记录权重key、输入值和结果值；端点方向先以A/B已知差分确认；不存在的层单列不适用。')]
    elif k in ['LoraSave','CLIPSave','ImageOnlyCheckpointSave','ModelSave','CheckpointSave','SaveLoRA','VAESave']:
        rows=[case('使用独立临时前缀保存，再用对应Loader回读','文件存在、tensor键/shape可读取；回读后匹配的下游任务可运行。保存精度改变可造成数值误差，不要求文件字节相同。','记录扩展名、文件hash、权重key数、dtype及回读误差。'),case('只改filename_prefix或prefix；若存在rank则再独立改rank','前缀只改变路径；LoRA分解rank改变秩/文件规模与重建误差，不能承诺高rank在每张图更好。','固定源权重和diff；检查文件元数据，避免覆盖基准。')]
    elif 'Scheduler' in k:
        steps='steps' in p
        rows=[case('steps=10 → 20' if steps else '固定输入，记录输出SIGMAS',
              '常规完整时间表通常是steps+1项，含终止sigma；专用/截断时间表要按实现检查实际数量。要求有限数值、合理噪声范围，不能仅检验能采样。',
              '探针逐项导出SIGMAS，记录len、首值、末值、单调性；将实际公式核对后再签收。'),
              case('只改'+next((x for x in ['rho','denoise','sigma_max','alpha','shift','max_shift','mu'] if x in p),'模型家族/分辨率条件')+'，先用默认值及一个邻近合法值',
              '时间表的分布/覆盖区间发生对应变化，未改的模型与采样算法保持。不能从sigma曲线直接推出画质一定改善。',
              '叠加两条sigma曲线；再用相同噪声做一对采样，记录耗时/失真，恢复A值验证可复现。')]
    elif g=='B09' or k in ['SamplerARVideo','VOIDSampler']:
        knob=next((x for x in ['eta','s_noise','order','num_frame_per_block','scale_ratio','version'] if x in p),None)
        rows=[case('接入同一SamplerCustomAdvanced链路；替换为该SAMPLER','输出latent形状符合该算法/模型要求；记录每步模型求值与时间。算法不同不保证同seed画面相同或质量更好。','基线固定NOISE、Guider、SIGMAS、latent；用同一输出解码器。'),case(('仅改'+knob+'，按下表默认值及邻近合法值') if knob else '旁路算法对照与本算法各跑一次','eta/s_noise用于随机噪声时，减到0可关闭对应随机项；order影响数值方法而非图像尺寸；AR块长影响分块数量；scale_ratio为例外，会放大空间尺寸。无此参数的节点仅做替换对照。','选择与实际参数相符的判据；记录shape、噪声差异/模型求值，不混用不同算法含义。')]
    elif g=='G04' or k=='WanAnimate2Cache':
        knob=next((x for x in ['reuse_threshold','max_gpus','dtype','device','backend'] if x in p),'是否接入补丁')
        rows=[case('绕过优化与启用优化；各warmup一次后运行3次','输出shape/时长应保持；数值允许取决于优化的偏差。可能加速也可能不加速，硬件不满足不判为功能失败。','记录模型加载之外的耗时中位数、峰值显存、输出MAE；标明缓存是否真的重用。'),case('只改'+knob+'为另一支持配置','实际计算设备/精度/复用率应与策略对应；同等输出规模下对照成本和误差。高阈值复用通常更多但误差可能增加。','不能把ComfyUI整节点缓存命中当算子加速；确认目标节点实际重跑。')]
    elif g=='G02':
        knob=next((x for x in ['strength_model','strength','apply_to_conds','schedule_clip','set_cond_area'] if x in p),'hook/condition输入')
        rows=[case('一个hook/condition → 两个可识别对象','组合节点保留对应两组条目，属性节点写入对应mask/时段/强度；原始对象应仍可用于未修改基线。','查条目标识和metadata，再采样，不能只检查对象非空。'),case('只改'+knob+'；数值用中性值与默认值，开关用false/true','相应分支的权重/绑定/时段发生变化；未涉及的条件条目不应被意外移除。源码未明确的重复hook合并优先级单列探索。','打印每个hook的生效区间与强度；固定随机噪声做A/B。')]
    elif g in ['B10','G01','E24'] or 'MODEL' in out and any(x in p for x in ['strength','scale','model_patch']) or k in ['CLIPAttentionMultiply','CLIPSetLastLayer','T5TokenizerOptions','FluxDisableGuidance','FluxGuidance']:
        knobs=[x for x in p if p[x]['type'] in ['FLOAT','INT','BOOLEAN','COMBO']]
        knob=next((x for x in ['strength','scale','multiplier','cfg','shift','q','stop_at_clip_layer','min_length'] if x in p),knobs[0] if knobs else '补丁接入')
        rows=[case('原MODEL/CLIP/条件支路与经节点支路对照','输出接口保持兼容；补丁本身不产出图片。必须在编码或采样时实际消费才能看到效果。零值是否中性由该算法决定，不能通用设0。','保存相同seed的下游结果，记录修改的层/时段/设备配置。'),case('只改'+knob+'：默认值→邻近合法值→恢复默认','对应预测/条件/注意力/采样映射改变；最终shape通常保持（下采样/上下文补丁另查中间shape）。效果/速度/质量不保证单调。','观察对象中对应配置，并配对5seed记录提示词符合率、伪影、耗时；只看最终图不能证明指定层生效。')]
    elif k.startswith('Empty'):
        dims=[x for x in ['width','height','length','seconds','batch_size','resolution','layers','frames_number'] if x in p]
        axis=next((x for x in ['batch_size','width','seconds','length','resolution','layers'] if x in p),dims[0] if dims else None)
        rows=[case('运行下表默认参数，先只构建latent','得到当前模型家族要求的LATENT；记录每个samples分支的B/C/T/H/W、dtype和有限值。Empty并不统一意味着所有张量都为零或4通道。','查shape和数值范围，与匹配模型/VAE最小消费者契约对照。')]
        if axis:
            expected={'batch_size':'batch_size=1→2时，批次维从1变2，单项空间/时间尺寸保持。','width':'width取两个合法整倍数（如默认与默认+一个步长），空间宽度按本模型压缩率改变；视频时长保持。','seconds':'seconds取两个合法时长；音频latent长度/解码样本数跟随时长，取整由音频VAE网格决定。','length':'length取两个相邻合法帧网格，时间轴增加；空间宽高保持；不要把latent时间格数量当作最终视频帧数。','resolution':'resolution改变三维网格/潜空间分辨率；batch保持；体素空间三个轴应按定义变化。','layers':'layers改变层轴数量；每层宽高保持；不能把它当batch_size。'}
            rows.append(case('只改'+axis,expected.get(axis,'对应轴按输入改变，其余未指定轴保持。'),'探针记录前后shape；由匹配解码器核对最终帧数/尺寸，超预算时只做latent构建。'))
    elif any(x in k for x in ['TextEncode','TextGenerate']) or k=='CLIPTextEncode':
        fields=[x for x in p if p[x]['type']=='STRING' and x not in ['system_prompt','language','keyscale']]
        rows=[case('只把描述red cube on white background改为blue sphere on white background；字段：'+', '.join(fields),
              '编码节点：条件embedding/metadata应随文本改变，非直接输出图片；生成文本节点：实际返回文本。下游生成更倾向对应颜色/物体，但不是必然。',
              '固定CLIP和模型；记录条件shape/数值摘要，5seed统计对象/颜色/背景三项，不能只改token长度同时换模型。'),
              case('恢复原文本，所有采样配置/参考输入保持','纯编码同环境应可复现；自回归/音乐/文本生成编码涉及内部随机时还须固定其seed/采样策略。','比较输出embedding或文本，记录内部seed是否暴露；没有暴露则标随机而非失败。')]
        if any(x in p for x in ['image','image1','images']):
            rows.append(case('编辑指令固定，只换参考图红方块→蓝球','参考条件应改变；输出更倾向保留参考主体/布局并执行同一编辑，不要求逐像素复制。','同一个参考端口、相同数量和分辨率；先检查条件中参考数，再看生成。'))
    elif k.startswith(('VAE','Vae')) or k in ['LTXVAudioVAEDecode','LTXVAudioVAEEncode','StableCascade_StageC_VAEEncode','AudioEncoderEncode','WanDancerEncodeAudio','CLIPVisionEncode']:
        rows=[case('固定输入与匹配编码器/解码器运行','返回对应类型/数量且数值有限；音频检查采样率、通道、样本数；3D检查体素/网格/点数与bounds；视觉编码检查embedding shape。编码不能直接当成可播放媒体。','逐个输出接正确消费者；记录转换前后维度与模型hash。'),case('只改变输入内容或本节点的分辨率/数量参数','音频内容改变应影响特征而不应擅自改变时长；3D num_gaussians等数量参数应反映在计数；分块num_chunks主要影响执行分块/显存。','按实际存在参数做一次独立对照；相同参数恢复后复查；有损VAE不要求原始信号精确重建。')]
    elif 'CONDITIONING' in out or any(x in k for x in ['ToVideo','ToVideoLatent','ToVideoInplace']):
        refs=[x for x in p if p[x]['type'] in ['IMAGE','AUDIO','LATENT','CLIP_VISION_OUTPUT','BBOX','MASK'] and x not in ['latent','samples']]
        strength=next((x for x in ['strength','pose_strength','guidance','audio_scale','noise_augmentation'] if x in p),None)
        rows=[case('固定所有模型，按输入表连接基准条件，保存条件摘要','必须产出下表声明的端口；正负条件、latent、音视频分支的返回数量按当前节点逐一核对。不允许假设每个条件节点都同时输出positive/negative/latent。','记录每个CONDITIONING条目数、shape、metadata key、引用帧号及latent各轴。'),
              case('仅替换参考输入 '+(', '.join(refs)+' 中的一项' if refs else '或一个区域/时长/指导配置'),
              '对应参考/区域/时序metadata改变；生成的参考符合程度只能统计比较，不能保证整幅画面逐像素跟随。参考类型必须与模型家族匹配。',
              '用明显不同且合法的两份参考；同5seed比较参考主体、布局/动作/声音中的目标属性。若只改时间配置，直接查时间字段。')]
        if strength:
            rows.append(case('仅改'+strength+'为默认值与一个邻近合法值','该条件/噪声/引导权重发生变化；若源码明确0是关闭，可补0组。不能把所有strength/noise_augmentation都解释为越大越贴近参考。','记录直接条件权重或噪声幅度；配对结果分开评价符合程度与伪影。'))
    elif 'LATENT' in out or 'NOISE' in out:
        rows=[case('诊断输入每帧/切片带编号；通过本节点','输出张量维度、帧顺序、noise_mask等元数据符合此操作；必须逐轴记录，不能只看LATENT类型相同。','查输入输出shape/编号；用对应解码器辅助观察。'),case('只改变本节点的一个时序/空间/噪声输入，恢复后再跑一次','裁切/替换应作用于明确区间，区间外编号保持；生成噪声应固定随机种子可复现；分块合并应保序且不丢帧。','按本节点名称选择操作；具体参数单位/轴未从源码确认前标待核对，不能标PASS。')]
    else:
        return None
    return {'setup':setup,'cases':rows,'kind':kind}

def slug(k):
    return quote(k, safe='-_.').replace('%','_')

def esc(s):
    return str(s).replace('|','\\|').replace('\n','<br>')

def focused_trials(n):
    """Concrete legal sweeps for selected family parameters, not all combinations."""
    k=n['class_name'];out={o['type'] for o in n['outputs']};p={i['name']:i for i in n['inputs']}
    priority=['strength_model','strength','cfg','guidance','steps','width','length','seconds','batch_size','seed','noise_seed','eta','s_noise','rho','reuse_threshold','max_gpus','stop_at_clip_layer','min_length','start_percent','end_percent','scale','shift','multiplier']
    trials=[]
    for name in priority:
        if name not in p:continue
        i=p[name]
        m=re.search(r'默认 (-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)',i['hint'],re.I)
        if not m:continue
        default=float(m[1]);mn=re.search(r'最小 (-?\d+(?:\.\d+)?)',i['hint']);mx=re.search(r'最大 (-?\d+(?:\.\d+)?)',i['hint']);st=re.search(r'步长 (\d+(?:\.\d+)?)',i['hint'])
        lo=float(mn[1]) if mn else -float('inf');hi=float(mx[1]) if mx else float('inf');step=float(st[1]) if st else (1 if i['type']=='INT' else .1)
        delta=max(step,round(abs(default)*.25/step)*step)
        vals=sorted(set(round(max(lo,min(hi,default+x*delta)),6) for x in [-1,0,1]))
        if name in ['seed','noise_seed']:vals=[123,124,123]
        elif name=='batch_size':vals=[1,2] if lo<=1 and hi>=2 else vals
        if len(set(vals))<2:continue
        values=' → '.join(format(v,'g') for v in vals)
        exp=None;obs=None
        if name in ['seed','noise_seed']:
            exp='固定其余输入时，恢复123应回到基准随机过程；124通常改变随机结果，输出shape保持。';obs='确认运行后seed控制为fixed；A/B/A′对照，不能以缓存命中证明重算。'
        elif name=='width':
            exp=('输出latent的空间宽轴应按本模型压缩/对齐规则变化；高度与时间轴保持。先用匹配解码器检查最终宽度。' if 'LATENT' in out else '这是本节点的分辨率条件/配置；应改变对应width元数据或计算分布，不等于立即把输入IMAGE缩放。')
            obs='每次记录直接输出shape/对应metadata；取整规则未知时先核对模型配置，不能套用SD的8倍。'
        elif name in ['length','seconds']:
            exp=('目标帧数按模型合法时间网格对齐，视频帧数改变；空间尺寸保持。' if name=='length' else '目标音频时长改变；样本数约为时长×采样率，VAE分块/补齐需单列。')
            obs='导出实际帧数/样本数与时间戳；检查音画同步，不能只读播放器舍入秒数。'
        elif name=='batch_size' and k.startswith('Empty'):
            exp='样本批次从1变2；单项空间/时间轴不变，不能把batch与时间混淆。';obs='查samples的batch轴；联合latent逐分支检查。'
        elif name in ['strength_model','strength','scale','multiplier']:
            exp='所选模块/条件/补丁的系数改变；具体中性值由节点算法决定。可观察目标是配置/权重增量及固定输入的响应，画质没有通用单调方向。';obs=f'先查{name}进入的权重/condition/前向配置；再5seed记录目标属性分数和伪影。'
        elif name in ['cfg','guidance']:
            exp='条件指导系数或guidance embedding改变；它们不是同一个计算位置。形状保持；提示词符合率可能变化，高值也可能失真。';obs='直接检查配置/embedding；配对5seed记录对象/颜色/背景三项，不能仅看“更好看”。'
        elif name=='steps':
            exp='请求步数预算改变；调度器序列长度和采样器实际求值次数要分别统计，多步/自适应算法不等于每步只调用模型一次。';obs='记录len(SIGMAS)、实际模型求值次数和采样耗时；有denoise时保持其固定。'
        elif name in ['eta','s_noise']:
            exp='改变该算法对应随机项幅度；如果分支关闭或该算法不使用此项，输出可以不变。不能把它解释成输入图像强度。';obs='同noise_seed对照，查每步噪声注入开关与结果差值；shape不变。'
        elif name=='rho':
            exp='sigma插值曲率改变，sigma_min/max保持；中间点的数值应能按该调度公式逐项计算。';obs='输出完整SIGMAS列表，比较端点与中间点，不直接从rho推断画质。'
        elif name=='reuse_threshold':
            exp='缓存复用判据改变；更宽松时通常复用更多，速度与误差有取舍。';obs='固定warmup，记录复用次数/模型调用次数、3次耗时中位数、MAE。'
        elif name=='max_gpus':
            exp='允许设备数上限改变，实际参与数不能超过可用GPU和上限；不保证近似线性加速。';obs='少于所需GPU时标BLOCKED_RESOURCE，记录各卡显存和任务分配。'
        elif name=='stop_at_clip_layer':
            exp='提取CLIP不同末端层的表示，embedding shape通常保持、值改变；不是减少输出图片层数。';obs='同text对比embedding统计与固定生成链，不假定某一层永远更好。'
        elif name=='min_length':
            exp='短提示词的最小token填充长度可能改变；超过最小长度的长文本可能不变。';obs='同时测短/长文本token长度；不以生成图有无变化为唯一依据。'
        elif name in ['start_percent','end_percent']:
            exp='所选作用时间区间边界移动；按sigma映射判断生效步，不直接用percent×steps代替。';obs='确保start≤end；打印每步生效标志。与另一个边界冲突的数值跳过并记录。'
        elif name=='shift':
            exp='模型噪声/时间映射发生变化；输出分辨率/名义时长保持，质量不保证单调。';obs='记录对应sigma或t映射，再固定seed比较；不与scheduler同时改。'
        if exp:
            trials.append(case(f'单参数数值扫描：{name} = {values}（其它保持基准）',exp,obs))
        if len(trials)==3:break
    return trials

def render():
    records=[]; unknown=[]
    for n in SCHEMAS:
        k=n['class_name']; g=MEMBERS[k]
        spec=CASES.get(k) or family(n)
        if spec is None:
            unknown.append(k);continue
        path=f'nodes/{g["id"]}/{slug(k)}.md'
        rows=spec['cases'] + ([] if k in CASES else focused_trials(n))
        npath=ROOT/path;npath.parent.mkdir(parents=True,exist_ok=True)
        lines=[f'# {k}：可观察实验', '', f'[所属实验 {g["id"]}](../../{g["path"]}) · [逐节点目录](../README.md) · [测量与判定](../../guides/observable-results.md)', '',
               '**状态：实验设计，未执行。** 下面是待检验的预期，不是已经获得的结果。标注“核对/探索”的分支需先确认本机实现，不能因没报错就签收。', '',
               '## 基准与接线', '', spec['setup'], '',
               '先完成所属实验的前置依赖。以下未列为变量的参数使用本机默认并截图保存；每次只改用例指定的一项。多种节点共用的实验中，只执行本节点实际具有的参数/操作。', '',
               '## 可观察的预期与参数对照', '', '| 用例 | 唯一变化/操作 | 预期结果 | 怎么观察、如何判定 |','|---|---|---|---|']
        for j,r in enumerate(rows,1):lines.append(f'| {g["id"]}/{k}/{j:02d} | {esc(r["change"])} | {esc(r["expected"])} | {esc(r["observe"])} |')
        lines += ['', '## 实际输入清单', '', '此表来自固定版本索引；不是所有参数组合均已覆盖。动态下拉/动态增长端口必须在本机展开并补录子字段，顶层名字不能代表其所有分支。hidden字段由运行时提供，不作为手填实验变量。', '', '| 输入 | 类型 | 必需性 | 索引中的默认值/范围/提示 |','|---|---|---|---|']
        for i in n['inputs']:
            if i['required']!='hidden':lines.append('| '+ ' | '.join(esc(i[t]) for t in ['name','type','required','hint'])+' |')
        if not [i for i in n['inputs'] if i['required']!='hidden']:lines.append('| 无用户输入 | — | — | 用上游输入变化或下游消费者验证，不虚构参数。 |')
        lines += ['', '## 输出检查点', '', '| 输出端口 | 类型 |','|---|---|']
        for o in n['outputs']:lines.append(f'| {esc(o["name"])} | {esc(o["type"])} |')
        if not n['outputs']:lines.append('| 无数据输出 | 检查UI预览或实际落盘副作用 |')
        lines += ['', '## 验收与记录', '',
                  '逐用例记录 `PASS / FAIL / BLOCKED / INCONCLUSIVE`，附A/B参数、工作流、实际输出和证据。确定性项按数值/形状/位置核对；随机生成项按预先定义的属性计分。没有变化时先排除缓存、未连接消费端、输入缺乏对比特征、错误分支和未加载权重。', '',
                  '若用例需要查看tensor/metadata而目前只有图片预览，该项记 `BLOCKED_OBSERVATION`。不要用“看起来差不多”替代张量级断言；可按[测量指南](../../guides/observable-results.md)在源码断点读取。', '',
                  '复制[结果模板](../../templates/node-experiment-record.md)到 records；初始环境/基准失败时先修复，后续参数对照暂不执行。', '',
                  '## 依据与版本', '',
                  f'- 索引模块：`{n["module"]}`。接口依据：[固定索引快照](https://github.com/wanghuaiqing2023-blip/comfyui-learning-hub/blob/3e2e4c43e778e41a9bc577edd8ee3d25ad095471/docs/01-%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8/ComfyUI-%E7%B3%BB%E7%BB%9F%E5%AD%A6%E4%B9%A0%E6%89%8B%E5%86%8C/%E8%8A%82%E7%82%B9%E6%89%8B%E5%86%8C/03-%E5%85%A8%E9%83%A8%E5%86%85%E7%BD%AE%E8%8A%82%E7%82%B9%E7%B4%A2%E5%BC%95.md)。',
                  '- 行为预期含公式推导、接口契约和实验假设；不等于全部逐函数核实。已核对公式及版本差异见[依据清单](../../guides/expectation-sources.md)。', '']
        npath.write_text('\n'.join(lines))
        records.append(dict(class_name=k,experiment=g['id'],path=path,design='curated' if k in CASES else 'family',status='not_run',cases=rows))
    if unknown:
        print('UNASSIGNED:', ', '.join(unknown))
        raise SystemExit(1)
    (ROOT/'data/node-experiments.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    lookup={r['class_name']:r for r in records}
    index=['# 逐节点实验目录','','每个节点都有独立实验卡；先按[实验组依赖](../labs/README.md)准备上游，再执行卡内A/B对照。**所有用例尚未运行；覆盖设计不等于验证通过。**','','[测量规则](../guides/observable-results.md) · [结果模板](../templates/node-experiment-record.md)','']
    for g in GROUPS:
        index += [f'## {g["id"]} {g["title"]}', '', '| 节点 | 用例数 |','|---|---|']
        links=[]
        for k in g['nodes']:
            r=lookup[k]; index.append(f'| [{k}]({r["path"].removeprefix("nodes/")}) | {len(r["cases"])} |')
            links.append(f'- [{k}：预期结果与参数对照](../../{r["path"]})')
        index.append('')
        p=ROOT/g['path'];s=p.read_text();s=s.split('\n## 逐节点可观察实验卡')[0].rstrip()
        p.write_text(s+'\n\n## 逐节点可观察实验卡\n\n'+ '\n'.join(links)+'\n')
    (ROOT/'nodes/README.md').write_text('\n'.join(index))
    print(f'Rendered {len(records)} cards / {sum(len(r["cases"]) for r in records)} cases; curated={sum(r["design"]=="curated" for r in records)}')

if __name__=='__main__':render()
