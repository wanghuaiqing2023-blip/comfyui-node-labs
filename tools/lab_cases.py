"""Curated experiments. Predictions are designs, never execution results.

The renderer augments these with the original input schema and source provenance.
"""
CASES = {}

def add(names, setup, *rows):
    for name in names.split('|'):
        CASES[name] = {'setup': setup, 'cases': [dict(zip(('change','expected','observe'), r)) for r in rows]}

add('GetImageSize', '读取 P1：512×384 RGB 单张；准备同尺寸的三帧批次。',
    ('单张 → 三帧批次', 'width=512、height=384 不变；batch_size 从 1 变成 3。', '三个 INT 分别接 PreviewAny，逐项记录。'),
    ('仅把图片缩到 256×192', 'width=256、height=192；单张 batch_size 仍为 1。', '不要寻找 IMAGE 直通输出。'))
add('LoadImage|LoadImageOutput', '使用 P1、P2；LoadImage 从 input 选择，LoadImageOutput 从 output 选择。',
    ('P1 → P2（已知 alpha 的 RGBA 文件）', 'IMAGE 能显示彩色内容；P2 的 MASK 是 1-alpha：透明处白，不透明处黑。P1 无 alpha 的遮罩尺寸可能为固定回退尺寸，不以等于原图验收。', 'IMAGE→PreviewImage；MASK→MaskToImage→PreviewImage。'),
    ('换成蓝色图片 B', '预览内容由 P1 变成蓝色，不能仍为旧文件；宽高按文件实际值返回。', '刷新文件列表后选择，核对文件名与图像。'))
add('PreviewImage|SaveImage', 'P1 接目标节点；输出目录使用独立前缀 labs/A01/run01。',
    ('提交一次 P1', '预览显示四角和 TOP；SaveImage 还产生可回读的 PNG；PreviewImage 只产生临时预览，不应作为 output 持久保存的证据。', '读取落盘文件，检查 512×384；比较解码像素而非 PNG 文件字节。'),
    ('换蓝色图片 B；保存节点另改 filename_prefix', '内容变蓝；前缀变化只改变保存路径/名称，不应改变像素。自动计数后缀允许变化。', 'SaveImage 文件回读后与输入比较；预览节点只比显示。'))
add('ImageCompare', 'image_a=P1，image_b=P1；使用本机前端的比较控件。',
    ('两边同图；拖动分隔线', '分隔线经过处没有图像内容跳变。', '截图分隔线在 25%、75% 的状态。'),
    ('只把 image_b 换成反相 P1', '分隔线两边分别保留原图和反相图；移动线只改变可见区域。', '不能把比较界面的输出当作差值图或 IMAGE。'))
add('PreviewAny', 'source 接 PrimitiveInt，值 7。',
    ('7 → 9', '显示文本从 7 变为 9。', '读取预览文字。'),
    ('改接字符串 abc', '显示 abc；不应继续显示上一轮数字。', '复杂对象的文本摘要不保证包含完整张量数值。'))
add('PrimitiveInt|PrimitiveFloat|PrimitiveString|PrimitiveStringMultiline|PrimitiveBoolean|SeedNode|CustomCombo', '目标输出接 PreviewAny；字符串用 Abc，数值用合法的 7，布尔用 false；下拉项记录当前可选值。',
    ('只改变 value / seed / choice 中本节点实际存在的输入', '输出应等于新输入；多行字符串应保留换行，布尔应切换真/假。种子节点只输出数值，本身不生成图片。', '逐字或逐数值比较；seed 后续行为设为 fixed。'),
    ('恢复原值', '输出恢复到基准；不应出现累加或沿用上轮值。', '记录 A→B→A 三次输出。'))
add('ColorToRGBInt', 'color 选择纯红 #FF0000。',
    ('红 → 绿 → 蓝', 'RGB 整数依次为 16711680、65280、255；十六进制对应 FF0000、00FF00、0000FF（大小写/前缀以节点格式为准）。', '两个输出分别接 PreviewAny。'))
add('ComfyNumberConvert', 'value 输入 3.75，再输入 -3.75。',
    ('3.75 → -3.75', '整数转换应检查截断方向；若实现采用 Python int，则为 3/-3；浮点输出保留 3.75/-3.75。此分支规则需对本机源码确认后签收。', '读取所有数值输出，不能只看四舍五入后的 UI 显示。'))
add('CreateList|MergeTextLists', '输入依次为 A、B、C；对于文本列表使用 [A,B] 与 [C]。',
    ('增加第四项 D', '输出项数增加 1；前面 A、B、C 的顺序保持。', '逐项接文本预览/列表消费者，不将批次数误当列表项数。'),
    ('交换前两个输入', '前两个结果随之交换，其余项不变。', '记录完整顺序。'))
add('ResolutionSelector', 'aspect_ratio=1:1，megapixels=1，multiple=64。',
    ('megapixels=1 → 4', '宽高均为 64 的倍数；面积接近目标，受取整影响；宽高大约各翻倍，不能要求像素数精确等于百万。', '记录 W、H、W×H 和 W/H。'),
    ('1:1 → 本机支持的横向 16:9', 'W/H 接近 16/9，面积仍接近同一目标。', '检查 multiple 取整误差。'))
add('ComfyMathExpression', 'expression 使用本机支持的变量名；最小表达式先用 2+3*4。',
    ('2+3*4 → (2+3)*4', '结果 14 → 20。', '数值输出接 PreviewAny。'),
    ('合法表达式 → 不完整的 2+', '应报告解析/执行错误，不应无提示返回上次结果。', '记录错误位置；恢复表达式后能运行。'))
add('CurveEditor', '建立从 (0,0) 到 (1,1) 的线性曲线，接支持曲线输入的 GLSLShader。',
    ('线性曲线 → 增加中点 (0.5,0.75)', '端点保持；中间输入对应的曲线值上移。具体插值由当前曲线模式决定。', '用同一灰阶渐变作为查询输入，比较中灰区域；不要用随机图。'))
add('StringConcatenate', 'string_a=cat，string_b=dog。',
    ('delimiter="-" → " / "', 'cat-dog → cat / dog。', '逐字比较，包含空格。'))
add('StringLength', '输入 ASCII 字符串 cat；再输入 cat dog。',
    ('cat → cat dog', '3 → 7，空格也计数。', '输出接 PreviewAny；首轮避免 emoji 的字素/码点歧义。'))
add('StringSubstring', 'string=abcdef。',
    ('start=1,end=4 → start=2,end=4', 'bcd → cd；end 不包含。', '按 Python 切片语义逐字比较。'),
    ('start=4,end=4', '空字符串。', '用加前后标记的方法区分空字符串与未执行。'))
add('StringReplace|ReplaceText', '输入 cat cat；find=cat。ReplaceText 对列表 [cat cat,dog] 执行。',
    ('replace=dog → fox', 'dog dog → fox fox；列表中原本 dog 项不受 find=cat 影响。', '逐项逐字比较。'))
add('StringContains', 'string=Cat dog，substring=cat。',
    ('case_sensitive=true → false', 'false → true。', '布尔输出接 PreviewAny。'),
    ('substring=bird', '两种大小写模式都应 false。', '使用确实不存在的字符串。'))
add('StringCompare', 'string_a=Cat，string_b=cat；mode 选相等比较。',
    ('case_sensitive=true → false', '不相等 → 相等。', '核对输出布尔语义，切换 mode 后需按该比较运算重新预测。'))
add('TextToLowercase|TextToUppercase|CaseConverter', '输入 AbC 12；列表节点输入 [AbC 12,xyZ]。',
    ('小写转换 / 大写转换（按节点或 mode）', '小写结果 abc 12；大写 ABC 12；数字和空格不变。列表项数不变。', '逐字符比较。'))
add('AddTextPrefix', 'texts=[cat,dog]，prefix=X:。',
    ('prefix=X: → 空串', '[X:cat,X:dog] → [cat,dog]。', '逐项比较，数量保持 2。'))
add('AddTextSuffix', 'texts=[cat,dog]，suffix=:X。',
    ('suffix=:X → 空串', '[cat:X,dog:X] → [cat,dog]。', '逐项比较，数量保持 2。'))
add('StripWhitespace|StringTrim', '输入含真实空格的 "  cat dog  "；StringTrim 先选两端。',
    ('处理前 → 处理后', '两端空格去掉得到 cat dog；中间空格保留。', '在字符串两端拼接方括号后预览。'),
    ('再次处理结果', '结果不变（幂等）。', '比较两次文本。'))
add('TruncateText', 'texts=[abcdef,xy]。',
    ('max_length=4 → 2', '[abcd,xy] → [ab,xy]。', '检查短文本不会被补齐。'))
add('RegexMatch|RegexExtract|RegexReplace', 'string=cat12 dog34；regex_pattern=([0-9]+)；先关闭全部 flags。',
    ('保持表达式运行', 'Match 应命中；Extract 按所选模式返回 12 或 [12,34]；Replace 用 # 替换得到 cat# dog#（count=0 时替换全部）。', '分别记录布尔、提取结果或替换文本，不能把三种节点输出混同。'),
    ('regex_pattern 改为 ZZZ', 'Match 为 false；Replace 原样返回；Extract 的无匹配表示需记录本机约定（空串/空列表）。', '记录无匹配与错误的区别。'))
add('JsonExtractString', 'json_string={"name":"cat","count":2}，key=name。',
    ('name 的值 cat → dog', '提取结果 cat → dog，其它字段不影响结果。', '逐字比较。'),
    ('改为非法 JSON', '应报告解析错误或明确失败值，不能继续给出旧 cat。', '记录本机错误约定。'))
add('ConvertArrayToString|ConvertDictionaryToString', '数组 [1,"cat"] 或字典 {"name":"cat","count":2}。',
    ('只改变 indent', '空白/换行发生变化，重新解析后的 JSON 值保持相等。', '用 Python json.loads 比较，不比较空白。'))
add('StringFormat', 'values 依本机动态端口提供 name=cat；f_string={name}。',
    ('{name} → pet:{name}', 'cat → pet:cat。', '若端口使用位置参数则改用 {0}，记录实际绑定。'),
    ('引用不存在的变量', '明确格式化失败，不得输出旧结果冒充成功。', '保存错误；恢复变量后重新运行。'))
add('BuildJsonPromptIdeogram', '仅填 high_level_description=red cube；其它字段留空或默认。',
    ('red cube → blue sphere', '输出可被 JSON 解析，描述字段更新；并不直接产生图片。', '检查字段值；字段缺省形式以源码定义为准。'))
add('SaveText', 'text=cat 后接真实换行再写 dog；filename_prefix=labs/text/run01。',
    ('text 中 cat → fox', '文件 UTF-8 解码后第一行 fox、第二行 dog。', '读取实际文件，扩展名与 format 一致。'),
    ('仅改变 filename_prefix', '内容完全相同，路径/名称不同。', '文件计数后缀可以变化。'))
add('TextOverlay', 'P1 叠加 LAB；font_size 先用 24。',
    ('font_size=24 → 48', '文字覆盖的像素区域变大，底图尺寸不变；不能要求字框恰好两倍（字体度量影响）。', '比较非文字区域与文字边界。'),
    ('text=LAB → 空串', '叠字消失，底图保留。', 'PNG 回读对比。'))
add('ComfyAndNode|ComfyOrNode', 'values 输入两个布尔值。',
    ('依次测试 false/false、false/true、true/false、true/true', 'AND 结果 F,F,F,T；OR 结果 F,T,T,T。', '逐行记录真值表。'))
add('ComfyNotNode', '输入布尔值。',
    ('false → true', '输出 true → false。', 'PreviewAny。'))
add('ComfySwitchNode', 'on_false=red，on_true=blue。',
    ('switch=false → true', '输出 red → blue。', '先用字符串验证分支选择；惰性执行是否跳过未选分支另查日志，不能由值推出。'))
add('ImageCrop|CenterCropImages|RandomCropImages|ImageCropV2', 'P1=512×384；裁剪目标 256×192；ImageCrop 起点 x=0,y=0；V2 在 crop_region 设置同一矩形。',
    ('运行基准裁剪', '输出 256×192；普通裁剪左上像素对应原图 (0,0)；中心裁剪对应 (128,96)；随机裁剪必须是原图某个连续窗口。', 'GetImageSize + 四角/坐标图案检查。'),
    ('宽度 256 → 128，保持其它条件', '输出宽 128、高 192；区域不能拉伸填满旧宽度。随机裁剪更换 seed 后位置可能改变，但不是每个 seed 都必须不同。', '记录输出边界在原图中的位置。'))
add('ImageScale', 'P1；upscale_method=nearest-exact；crop=disabled。',
    ('width=256,height=192 → width=512,height=192', '尺寸 256×192 → 512×192；第二组横向相对拉宽。', 'GetImageSize；对照圆形或方格宽高比。'),
    ('width=256,height=256；crop=disabled → center', '两组都是 256×256；disabled 改变长宽比；center 先取中心对应比例再缩放，左右部分内容被裁去。', '比较四角标记是否保留。'),
    ('width=0,height=192', '保持比例得到 256×192；0 表示自动推算该边。', '本项只适用于本节点，不能推给其它宽度参数。'))
add('ImageScaleBy', 'P1；使用 nearest-exact。',
    ('scale_by=1 → 0.5 → 2', '512×384 → 256×192 → 1024×768；比例保持。', '尺寸精确检查；不要以放大后更清晰验收。'))
add('ResizeImagesByLongerEdge|ImageScaleToMaxDimension', 'P1=512×384；目标长边使用 256。',
    ('目标长边 256 → 1024', '256×192 → 1024×768，比例 4:3。', '读取尺寸和长边；目标参数用本节点实际名称。'))
add('ResizeImagesByShorterEdge', 'P1=512×384。',
    ('shorter_edge=192 → 384', '256×192 → 512×384，比例 4:3。', 'GetImageSize。'))
add('ResizeAndPadImage', 'P1；target_width=512,target_height=512；padding_color 选黑。',
    ('黑边 → 白边', '尺寸始终 512×512；原图等比例放入，缺少的 128 像素高度由上下留边补齐；留边颜色随参数改变。', '比较图像区域与上下边带，中心对齐时各 64 像素。'))
add('ImageFlip|LatentFlip', 'IMAGE 用 P1；LATENT 用 P1 经匹配 VAE 编码；记录翻转前结果。',
    ('水平翻转 → 垂直翻转', '水平时左右角标交换；垂直时上下角标交换；输出尺寸不变。LATENT 应在张量层验证，解码边缘允许 VAE 差异。', '再执行同一种翻转两次，应恢复原张量/原图。'))
add('ImageRotate|LatentRotate', 'P1 及其 VAE latent；先选菜单中的 90 度。',
    ('90 度 → 180 度', '90 度交换空间宽高；180 度恢复原宽高但上下左右角标对换。方向以本机枚举定义为准。', '四次 90 度应恢复原排列；LATENT 先比较张量。'))
add('ImagePadForOutpaint', 'P1；left/top/right/bottom=0；feathering=0。',
    ('left=64，其它边=0', '输出 576×384；原图从 x=64 开始；新增带在左侧。新增区域 MASK 与保留区应区分。', '图片与 MASK 分别预览。'),
    ('feathering=0 → 16', '画布尺寸不变；接缝附近遮罩出现过渡带。', '比较 MASK，不用扩散结果判断羽化。'))
add('ImageStitch', 'image1=512×384 红图，image2=同尺寸蓝图。',
    ('direction=right，spacing_width=0 → 16', '宽从 1024 变为 1040，高 384；中间出现 16 像素间隔。', '量尺寸和间隔颜色。'),
    ('断开可选 image2', '输出与 image1 一致。', '逐像素比较。'))
add('AdjustBrightness', '灰阶测试图含像素 x=64/255、128/255、192/255。',
    ('factor=1 → 0.5', '按 clamp(x×factor,0,1) 计算：三个值减半。', '比较浮点张量；PNG 量化允许 1/255。'),
    ('factor=2', '前两档约 128/255、1；最高档也截到 1；高光会饱和。', '检查高光不是无限增长。'),
    ('factor=0', '所有像素黑，尺寸不变。', '检查 min=max=0。'))
add('AdjustContrast', '同一灰阶图。',
    ('factor=1 → 0', '公式 clamp((x-0.5)×factor+0.5,0,1)；0 时全部变为 0.5 灰。', '张量 min=max=0.5；PNG 量化有舍入。'),
    ('factor=0.5 → 2', '低于 0.5 的值向更暗方向扩大偏差，高于 0.5 的值向更亮方向扩大偏差；超界截断。', '用公式计算每档，不以整图平均亮度判断。'))
add('NormalizeImages', '灰阶梯度；mean=0.5,std=0.5。',
    ('输入 0、0.5、1', '输出 -1、0、1；本节点不是把图自动限制到 [0,1]。', '需张量探针；保存 PNG 会截断负值，不能作为此项证据。'),
    ('std=0.5 → 1', '相同 mean 下所有结果幅度减半；shape 不变。', '按 (x-mean)/std 核对。'))
add('ImageInvert|InvertMask', '灰阶图/遮罩含 0、0.25、0.5、0.75、1。',
    ('执行一次', '对应变为 1、0.75、0.5、0.25、0。', '按 1-x 检查。'),
    ('同一节点串联两次', '恢复原值；尺寸不变。', '张量最大绝对误差 ≤1e-6；PNG 比较允许量化。'))
add('ImageBlend', '两张同尺寸纯色：image1=红 (1,0,0)，image2=蓝 (0,0,1)；blend_mode=normal。',
    ('blend_factor=0 → 0.5 → 1', '红 → (0.5,0,0.5) → 蓝；公式 (1-f)A+fB。', '取中心像素，PNG 误差 ≤1/255。'),
    ('blend_mode=normal → multiply；factor=1', '红×蓝为黑；不能沿用 normal 的插值公式解释模式内部混合。', '取中心像素。'))
add('ImageAddNoise', '固定 P1；seed=123。',
    ('strength=0 → 0.1', '0 时为原图；0.1 时产生噪声，尺寸不变；平坦区差值标准差增大。', '原图与结果差值统计；是否裁剪影响边界像素。'),
    ('相同 seed 重跑；再换 124', '同环境同输入重跑可复现；更换 seed 通常改变噪声图案，不表示画质改善。', '确认实际执行而非缓存，再比较像素差。'))
add('ImageBlur|ImageSharpen', '一条黑白阶跃边缘 + 棋盘格；分别单独测试模糊或锐化。',
    ('半径从本机最小有效值增至 3', '模糊：边缘过渡带通常变宽、细棋盘对比下降；锐化：边缘局部对比可增大并产生光晕。不能把两节点方向混用。', '沿同一水平线读像素剖面；尺寸不变。'),
    ('恢复基准半径/alpha', '结果恢复基准；常量色块内部不应凭空出现结构。', '用常量灰图做对照，边界填充区单列。'))
add('Canny', '输入固定灰阶图：含一条强边缘和一条弱边缘；保存基准。',
    ('low_threshold/high_threshold 同比例提高，保持 low≤high', '弱边缘可能消失；强边缘较易保留；不能断言白像素数在每张图上严格单调。', '分别检查已知强/弱边缘的位置与连通性。'),
    ('输入改为均匀灰图', '没有内部真实边缘；图框算法边界单列，不应出现棋盘状内部边缘。', '排除外边框后统计。'))
add('ImageQuantize', '灰阶渐变加四色区域；先关闭 dither。',
    ('colors=16 → 4', '调色板颜色数上限降低，渐变色带更明显；每张输出的唯一颜色数不超过设定数。', '按 RGB 唯一值计数。'),
    ('保持 colors，只启用另一抖动方式', '局部像素分布变化；颜色数仍受调色板限制；不应据此认定新增真实细节。', '放大渐变区比较点状分布。'))
add('ImageHistogram', '同尺寸纯黑图、纯白图、水平灰阶渐变分别输入。',
    ('黑 → 白 → 渐变', '分布应由最低亮度端集中转为最高端集中，再展开；不能要求具体 bin 数，需读 HISTOGRAM 消费端定义。', '接支持 HISTOGRAM 的 CurveEditor/探针，记录横轴与计数总量。'))
add('ColorTransfer', 'image_target=冷色测试图；image_ref=暖色测试图；固定 method。',
    ('strength=0 → 1', '0 为原目标；1 应更接近所选算法的参考颜色统计，但几何边缘位置、尺寸保持。', '对比 RGB 均值/协方差或当前算法目标统计，不要求所有像素等于参考图。'))
add('ImageToMask|LoadImageMask', 'P1 的纯红、纯绿、纯蓝色块；LoadImageMask 从文件选择，ImageToMask 接图像。',
    ('channel=red → green', '红通道时红块白、绿/蓝块黑；绿通道时绿块白、红/蓝块黑。', 'MaskToImage 后取对应色块像素。'),
    ('alpha 通道（仅支持该选项的节点）', '需使用 P2；先确认该节点是否采用 1-alpha，不能把 RGB 通道规则直接套在透明度上。', '记录不透明和透明位置各一个值。'))
add('MaskToImage', '遮罩有 0、0.5、1 三个竖带。',
    ('转换为 IMAGE', '三个通道应相等，呈黑、灰、白；不改变宽高。', '检查 R=G=B=输入遮罩值。'))
add('SolidMask', 'width=512,height=384。',
    ('value=0 → 0.5 → 1', '全黑 → 全灰 → 全白；每个像素等于 value。', 'MaskToImage 预览；尺寸 512×384。'),
    ('只改 width=256', '输出 256×384；像素值仍等于 value。', '尺寸和值分开检查。'))
add('ThresholdMask', '水平线性灰阶遮罩；另用 SolidMask 精确构造 0.5。',
    ('value=0.25 → 0.75', '输出仅 0/1；白区收缩，边界向亮的一侧移动。', '公式：mask > value 为 1，其余 0。'),
    ('输入恰好 0.5，阈值=0.5', '全部为 0，因为比较是严格大于，不是大于等于。', '此精度测试使用 SolidMask 浮点输出，不用 8bit PNG 的近似中灰。'))
add('GrowMask', 'M1：512×384；白矩形 x=[128,384),y=[96,288)；tapered_corners=false。',
    ('expand=0 → 8 → -8', '白区包围盒 256×192 → 272×208 → 240×176；本例远离画布边界，无截断。', '统计白区 bbox；不把羽化灰区当边界。'),
    ('expand=8，tapered_corners=false → true', '角部形状由方形膨胀变为受十字邻域影响的切角；外接框大小相同。', '放大四个角比较。'))
add('FeatherMask', '先用全白 SolidMask=512×384；四边参数=0。',
    ('left=16，其它为 0', '第 x=0 列为 1/16，x=15 列为 1，其后仍为 1。', '检查沿水平线的值；这是画布边缘羽化。'),
    ('换用中央白矩形 M1，仍 left=16', '中央白矩形不应被柔化，因为它不接触左侧 16 像素带。', '避免把此节点误解为对任意白色轮廓做高斯模糊。'))
add('CropMask', 'M1；x=128,y=96,width=256,height=192。',
    ('基准裁剪 → x=0,y=0（尺寸保持）', '基准全白；改起点后只有原矩形与裁剪框相交部分为白。', '输出始终 256×192；按矩形交集检查。'))
add('ImageCompositeMasked|LatentCompositeMasked', 'destination=蓝图，source=红图，同尺寸；mask 全 0/0.5/1。LATENT 使用对应编码并先检查张量。',
    ('mask=0 → 0.5 → 1', 'IMAGE 分别为蓝、等比例红蓝混合、红；LATENT 为对应张量加权，解码颜色不保证线性。', 'IMAGE 按逐像素权重计算；LATENT 不用 RGB 值作为张量混合证据。'),
    ('source 小于 destination；x=0 → 64', '覆盖区域沿 x 移动 64 像素（LATENT 坐标换算按模型/实现）；范围外保持 destination。', '先固定 resize_source=false；单独核对尺度换算。'))
add('MaskComposite', '两个同尺寸二值矩形，部分重叠；x=y=0。',
    ('operation=add → multiply → subtract', '分别检查并集（裁到1）、交集、destination 去掉 source 区域；值保持 [0,1]。', '各取 A独有/B独有/重叠/背景四点。'))
add('SplitImageWithAlpha|JoinImageWithAlpha', 'P2 有不透明、半透明、全透明三带。LoadImage分别提供RGB与MASK；先接Join构造RGBA，再Split，不能把LoadImage的RGB输出假装成RGBA。',
    ('Split 后将对应 RGB/MASK 直接接 Join', '应恢复原 alpha 语义与 RGB；ComfyUI 的遮罩可能是反 alpha，不手动翻转两次。', '保存 RGBA 后检查 alpha 数组；RGB 不可见区域也单独记录。'),
    ('Join 的 alpha 输入分别使用全0与全1遮罩', '本次核对版本中内部alpha=1-mask：输入全0得到完全不透明，输入全1得到完全透明。', '不能只看黑色背景上的预览判断透明。'))
add('ImageBatch|BatchImagesNode|BatchMasksNode|BatchLatentsNode|LatentBatch|MergeImageLists', '三项用不同颜色或编号 A、B、C；形状一致；相应类型的入口分别准备。',
    ('输入 A,B → A,B,C', '结果项数由 2 变 3，顺序保持 A,B,C。列表和张量 batch 的容器结构分别记录。', '逐帧/逐项导出，不用一张拼图冒充 batch shape。'),
    ('交换 A 与 B', '前两项顺序对调，内容本身不变。', 'LATENT 先查张量，再解码抽查。'))
add('ImageFromBatch|LatentFromBatch', '输入三项 A,B,C；batch_index=0,length=1。',
    ('batch_index=0 → 1 → 2', '依次得到 A、B、C；每次 batch=1。', '逐项预览/解码。'),
    ('batch_index=1,length=2', '得到 B,C，顺序不变。', '越界行为另列探索，不能误当正常用法。'))
add('RepeatImageBatch|RepeatLatentBatch', '输入 A,B 两项。',
    ('amount=1 → 3', '项数 2 → 6；按整批重复应为 A,B,A,B,A,B。', '逐项检查，区分与 A,A,A,B,B,B 的重复方式。'))
add('RebatchImages|RebatchLatents', '输入 5 项编号 0..4。',
    ('batch_size=1 → 2', '第二组形成 2、2、1 的分组；总项数仍 5、顺序不变。', '记录每个输出批次 shape 和编号。'))
add('ImageGrid', '4 张 64×64 图片编号 0..3；cell_width=cell_height=64,padding=0。',
    ('columns=2 → 4', '2×2 网格为128×128；一行4列为256×64；编号无遗漏/重复。', 'GetImageSize 和编号位置检查。'))
add('ImageDeduplication', '列表 [A,A,B]；B 与 A 图案结构明显不同，避免只换颜色（感知哈希可能忽略颜色）。',
    ('默认 similarity_threshold', '完全重复 A 应合并；非重复 B 是否保留取决于感知相似度，记录阈值。', '检查保留项及首次出现顺序。'),
    ('阈值降低', '更容易被判相似，保留项通常不增加；这是相似性判定，不是像素相等去重。', '同一输入扫描阈值并记录保留数。'))
add('SplitImageToTileList|ImageMergeTileList', 'P1；tile_width=256,tile_height=192,overlap=0；合并 final_width=512,final_height=384。',
    ('拆分再合并', '无重叠规则网格应有4块；合并应恢复512×384及四角位置。', '与原图逐像素比较。'),
    ('增大 overlap（小于块宽高）', '相邻块应共享输入区域；重建后接缝无错位。块数受步长/边界策略影响，先按实现算起点。', '保存每块坐标与边界；不随意固定块数。'))
add('EmptyImage', 'width=512,height=384,batch_size=1,color=红。',
    ('color 红 → 蓝', '整张图从红变蓝，尺寸不变。', '中心与四角像素均一致。'),
    ('batch_size=1 → 3', '三张同尺寸同色图；不是一张三倍宽图。', 'GetImageSize batch_size=3。'))
add('CreateVideo|SaveAnimatedPNG|SaveAnimatedWEBP|SaveWEBM', 'V1：24 帧编号00..23；fps=24；不接音频；保存或经 SaveVideo 输出。',
    ('fps=24 → 12 → 48', '帧数/顺序保持24；名义时长约1秒→2秒→0.5秒。编码时间基准允许一个帧间隔的误差。', '解封装查帧数、时间戳和首尾编号，播放器显示不是唯一依据。'),
    ('只替换第12帧为蓝图', '对应帧发生变化，其它帧顺序不变；有损编码可能有邻帧像素误差。', '按帧号查看；PNG 无损与有损视频分开验收。'))
add('LoadVideo|GetVideoComponents|SaveVideo', '使用已经保存的 V1：24帧、24fps、无音频。',
    ('读取/拆分/保存回读', '24帧顺序00..23，fps≈24；没有音频不能伪造出波形。', '检查解封装组件；保存有损时只要求结构和编号一致。'),
    ('换成带 A1 音轨版本', '图像帧数/顺序保持；音轨可提取且采样率与时长可读取。', '记录 VIDEO、IMAGE、AUDIO 的区别。'))
add('VideoTemporalCrop|VideoRandomTemporalCrop|VideoFrameSample', 'V1=24帧00..23；首轮 num_frames/length=8。',
    ('连续裁剪 start_frame=4,length=8（随机节点固定seed；抽样节点固定strategy）', '确定性连续裁剪得到04..11；随机连续裁剪得到某8个连续编号；均匀抽样不要求连续但应覆盖时间范围。', '检查输出编号，不能只查数量。'),
    ('length/num_frames=8 → 4', '有效范围内数量变为4；连续裁剪仍保持连续顺序。', '越界和不足帧重复策略另查本机实现。'))
add('Video Slice', 'V1 按24fps封装；无音轨。',
    ('start_time=0.25,duration=0.5', '截取约第6帧起连续12帧，时长约0.5秒；边界由时间基准决定，允许1帧差异。', '读时间戳与首尾帧号。'),
    ('请求超过片尾，切 strict_duration', '应观察严格与非严格分支对不足时长的处理；错误/截断/补足须按实现记录，不能默认三者相同。', '此边界分支未源码确认，暂不作为通过项。'))
add('EmptyAudio', 'duration=1,sample_rate=48000,channels=1。',
    ('duration=1 → 2', '样本数48000→96000；波形全0。', '读取 AUDIO waveform.shape 与 sample_rate。'),
    ('channels=1 → 2', '通道数1→2；每通道时长不变。', '两个声道均全0。'))
add('AudioAdjustVolume', 'A1=1秒440Hz正弦，峰值0.1，48000Hz；避免削波。',
    ('volume=0 → +6 → -6 dB', '幅值倍数1→1.995262→0.501187；RMS 同比例；时长/采样率不变。', '直接测波形，公式 gain=10^(dB/20)；不要要求6dB精确两倍。'),
    ('先+6再-6', '在无编码/无裁剪的张量链路应恢复波形，误差≤1e-6。', '不能先经有损音频再要求精确往返。'))
add('JoinAudioChannels|SplitAudioChannels', '左声道A1=440Hz，右声道A2=880Hz；同采样率同长度。',
    ('Join 后 Split', '左右恢复原单声道；时长不变，两个通道不混音。', '测各通道频谱峰位置440/880Hz。'),
    ('交换左右输入', '左右频率对调。', '不能仅凭扬声器主观听感判断。'))
add('AudioConcat', 'A1=1秒440Hz，A2=2秒880Hz；同采样率/通道。',
    ('切换前后拼接 direction', '总时长始终3秒；440Hz与880Hz片段先后随方向交换。', '按时间窗口查看频谱，不应同时叠加。'))
add('AudioMerge', 'A1、A2均1秒，同采样率；峰值各0.1。',
    ('相加型 merge_method', '输出同时含440/880Hz；不是2秒串联。', '观察频谱两峰；幅值公式按所选方法核对。'),
    ('第二轨改为静音', '相加模式恢复第一轨；平均模式可能幅值减半，按模式分别预测。', '不要混用 sum/average 的端点预期。'))
add('TrimAudioDuration', '3秒音频：依次1秒440、880、1320Hz，48000Hz采样；已核对start_index虽然带index名称，单位实际是秒。',
    ('start_index=1,duration=1', '得到中间880Hz片段，样本数48000。', '测时长/频谱，不填48000作为开始秒数。'),
    ('start_index=0 → -1，duration仍为1', '分别得到开头440Hz和末尾1320Hz片段；负数从末尾计秒。', '截取范围超出片尾会截断；开始不小于结束会报错。'))
add('AudioEqualizer3Band', '含低/中/高三个频率的低幅度混合音；所有 gain=0。',
    ('仅 mid_gain_dB=0 → +6；中心频率对准中频', '中频附近能量提高，远离频段的分量变化较小；不是全带等比例增益。', '比较频谱，保留滤波过渡带。'),
    ('恢复全部 gain=0', '应恢复基准频谱/波形（允许滤波数值误差）。', '记录峰值，避免削波。'))
add('LoadAudio|PreviewAudio|SaveAudio|SaveAudioAdvanced|SaveAudioMP3|SaveAudioOpus|RecordAudio', 'A1=1秒440Hz；录音节点用麦克风录制短音并记录实际时长。',
    ('输入A1或录音并回放/保存回读', '能读到非零波形、采样率和声道数；A1主峰440Hz、时长约1秒。有损保存允许编码延迟，不能做逐样本相等验收。', '记录容器/编码器、时长、RMS；RecordAudio用拍手验证非静音输入。'),
    ('换成2秒880Hz A2', '时长约2秒、主峰880Hz；不能仍播放缓存旧音频。', '有格式/quality参数时另做文件大小和失真对照，不保证每个短文件大小单调。'))
add('VAEEncode|VAEEncodeTiled|VAEDecode|VAEDecodeTiled', '已知匹配的 SD1.5 VAE；P1=512×384，batch=1；构造 encode→decode 闭环。',
    ('基准往返', 'SD1.5 latent samples 为[1,4,48,64]；解码图512×384。往返是有损变换，不要求像素相等。', '探针查shape；保存原图/重建图，计算MAE并检查角标位置。其它VAE压缩率不可套此数字。'),
    ('P1改为256×192；或 tiled 节点单独缩小 tile_size', '换图尺寸时对应latent为[1,4,24,32]；仅改tile时输出整体尺寸保持，显存和接缝误差可能改变。', '每次只选一种变化；分块应同时记录峰值显存和接缝。'))
add('EmptyLatentImage', 'width=512,height=384,batch_size=1。',
    ('基准 → batch_size=2', 'samples.shape [1,4,48,64]→[2,4,48,64]；初始samples全0。', '探针查shape/min/max；空latent不是成品图片。'),
    ('width=1024，其它恢复基准', '[1,4,48,128]，只增加latent宽度。', '不要把通道数4推广到其它模型家族。'))
add('KSampler', '使用已跑通的 SD1.5 基线：512×512，batch=1，euler，normal，steps=20，cfg=7，seed=123 fixed，denoise=1；提示词 red cube on white background。',
    ('所有输入固定，重复运行，再 seed=124', '同环境重复运行应可复现（GPU非确定性单列）；换seed通常改变构图/纹理，尺寸保持512×512。', '分别保存结果，MAE对照；缓存命中不是重新计算证据。'),
    ('steps=10 → 20 → 30', '采样步数预算提高；耗时通常增加。画质和提示词遵循度没有必然单调关系。', '记录采样时间而非加载时间；同seed并排，评估对象/颜色/背景三项。'),
    ('cfg=1 → 4 → 8，steps固定', '普通CFG模型的条件/无条件组合权重改变；高值可能更强调条件，也可能过饱和/失真。', '用5个固定seed配对比较三项符合率及失真数；不能由一张图判定规律。'),
    ('输入改为已编码P1后，仅denoise=0 → 0.3 → 0.7 → 1', '0时latent保留；较高值通常允许更大改动，非严格单调。0组与P1的VAE往返图比较，不与原PNG要求相等。', '固定同一latent和seed；保存差值及内容变化。'))
add('KSamplerAdvanced', '已跑通的普通采样基线；固定相同噪声、模型、条件、总steps=20。',
    ('完整0..20步 → 分段0..10再10..20', '首段保留剩余噪声，第二段不重新加噪；对无额外随机性且可分段的采样器，结果应接近整段。多步算法重启会有历史差异，不能统一要求精确相等。', '先用euler验证；记录start/end、add_noise、return_with_leftover_noise。'),
    ('仅第二段重新加噪', '通常出现额外扰动，无法再把它当成同一完整轨迹的等价拼接。', '固定noise_seed，比较最终差值。'))
add('BasicGuider|CFGGuider|SamplerCustom|SamplerCustomAdvanced', '复用同一MODEL、条件、latent、RandomNoise=123、euler与20步SIGMAS；先跑通自定义采样链。',
    ('CFGGuider cfg=1 与 BasicGuider 使用同一正向条件对照', '对标准CFG实现且无其它补丁时，两者应接近同一条件预测路径；蒸馏/专用模型另按其接口验收。', '比较最终latent；BasicGuider不凭空增加negative端口。'),
    ('只换NOISE种子或实际存在的noise_seed', '采样结果通常改变，latent形状保持；只换guider时不能同时换噪声。', '记录所有独立对象的来源节点。'))
add('RandomNoise|DisableNoise|AddNoise', '准备全零latent和已知SIGMAS；用相同消费者实际生成/加入噪声。',
    ('随机seed=123重复，再124', '随机噪声同seed可复现、换seed通常不同；DisableNoise产生零噪声效果，与seed无关。', '在NOISE被消费者调用后看张量，不能对NOISE对象字符串做数值判断。'),
    ('AddNoise 输入换为DisableNoise', '新增随机噪声贡献应消失；模型的latent缩放/均值处理仍按实现记录。', '比较输入输出，不把所有模型都断言为简单x+n。'))
add('LatentAdd|LatentSubtract|LatentMultiply|LatentBlend|LatentInterpolate', '构造同shape张量A全1、B全3；可用诊断夹具，在CPU张量级验证，之后再接真实latent。',
    ('Add / Subtract / Multiply(multiplier=2)', '对应逐元素4 / -2 / 2；仅对实际测试的节点使用该预期。', '探针读samples；保留LATENT其它字段。'),
    ('Blend或Interpolate比例0/0.5/1', 'Blend通常线性端点A、B，中间为2；Interpolate可能含范数处理，必须按实现核对，不能直接承诺中间2。', '端点和中间值分开记录；未查实现的插值公式标待核对。'))
add('LoadLatent|SaveLatent', '已知samples形状的latent，带必要元数据；独立保存前缀。',
    ('保存后重新LoadLatent', 'samples形状和值应按保存精度恢复；额外字段是否保留逐项检查，不能仅凭能解码判通过。', '比较dtype、shape、最大误差和key列表。'),
    ('仅改filename_prefix', '保存路径变化，数值内容不应改变。', '不同文件同一VAE解码对照。'))
add('LoraLoader|LoraLoaderModelOnly', '已知与基础模型匹配的LoRA；固定提示词、噪声与采样器；先保存绕过LoRA的基准。',
    ('strength_model=0（存在strength_clip也置0）→ 0.5 → 1', '0应与绕过接近；非零增加参数增量，不保证风格强度或质量严格单调。', '同5个seed对照；确认日志中实际匹配到权重键。'),
    ('只改变模型强度，文本编码器强度固定', '可单独归因到模型分支；ModelOnly没有CLIP强度输出/输入，不可虚构。', '逐项记录实际端口。'))
add('ModelMergeSimple|CLIPMergeSimple', '两个相同架构的对象A、B；相同key与shape；只在副本上合并。',
    ('ratio=0 → 0.5 → 1', '已核对公式为r×A+(1-r)×B；端点依次为B、平均、A。CLIP的position_ids/logit_scale等排除键单列，不宣称整个对象替换。', '比较可合并权重；此方向和许多图像混合节点相反，不能凭ratio名字猜。'),
    ('A与A合并，ratio=0.5', '应恢复A，不产生额外效果。', '直接比较可合并参数。'))
add('BuildPoseFile', '固定24帧MHR姿态，单人抬手并侧移；另备2条有效track；连同一SAM3D_BODY_MODEL；GLB先用body_mesh；固定世界相机，关闭自动居中。',
    ('fps=12 → 24 → 48，其余完全相同', '关键帧间隔1/12→1/24→1/48秒；24帧首尾采样时间跨度23/fps，即1.916667、0.958333、0.479167秒。按N/fps计片段名义时长则为2、1、0.5秒，两种口径不能混淆。', '读取GLB animation时间accessor或BVH Frame Time；同帧姿态应保持，禁止只凭播放快慢。'),
    ('camera_translation=off → centered → absolute', 'off不烘焙预测相机平移；centered使用相对首帧位移，首帧增量0；absolute使用原始平移，可能有较大Z深度。这里只比较新增的平移项，不要求骨架root世界坐标为0。', '记录首/中/末帧root平移向量；固定相机截图。若输入平移恒定，centered看不出运动，应更换侧移素材。'),
    ('2条轨迹下track_index=-1 → 0 → 1', 'GLB分别导出全部/第一条/第二条；应能通过抬左手与抬右手动作辨别。BVH只支持单骨架，-1在已核对源码中退化为0。', '数人体实例/骨架并核对动作，不能只数mesh节点（单人可能多mesh）。'),
    ('format=glb → bvh；BVH units=m → cm', 'GLB可带网格/材质/骨骼动画；BVH为层级与运动，不保留材质。cm与m长度/平移数值应相差100倍，旋转与帧数不变。', 'BVH检查HIERARCHY、MOTION、Frames=24、Frame Time=1/fps；设置导入单位后比较世界尺度。'),
    ('MHR输入且无_skeleton_override；断开sam3d_body_model，选择bvh/body_mesh/bones_only', '应明确报告缺少模型/骨架，不应产出有效空文件；这些分支虽顶层optional，运行时仍有条件依赖。', '记录完整异常并恢复连接重试；此失败是预期负例。'),
    ('GLB mesh_style：body_mesh → bones_only → openpose/scail', '表示方式改变：皮肤网格、骨骼、关键点/连杆；相同帧的动作阶段仍对应。细分材质、骨骼半径、手脸开关须记录展开后的实际字段。', '核对几何/材质、关键帧与坐标，不把风格变化当成pose推理变化。'))
add('EmptyMiniMaxH3LatentAV', 'width=1344,height=768,length=124；只构建latent即可，不必先采样。',
    ('length=124 → 141', '合法帧网格17k+5；视频和音频两个分支的时间长度一起变化。名义时长124/24≈5.1667秒、141/24=5.875秒。', '用AV分离节点分别查shape，再在有模型时解码核对帧数/音频时长。'),
    ('通过API测试length=125（若当前前端只允许步长17）', '按索引的向上取整规则应归到141帧；这是边界探针，先核对当前temporal_shape实现。', '不能把UI拒绝输入当成取整失败。'))
add('MiniMaxH3AddGuide', '已跑通H3链路；保持原始AV latent；positive串过本节点；引导图片用明显不同的红/蓝参考帧。',
    ('frame_idx=0 → -1', '锚点从开头移到末尾；模型生成只预期附近更符合参考，不承诺逐像素复制。', '按对应帧窗口查看；该节点只输出CONDITIONING，不输出新LATENT。'),
    ('输入4帧引导 → 5帧 → 22帧', '按索引：少于5帧只取第一张；5/22为合法片段长度。音频会按剩余时长裁剪。', '先查条件元数据/源码，再观察生成片段；缺video/audio VAE分别作为条件依赖负例。'))
add('MiniMaxH3SigmaShift', '已跑通H3音视频同采样闭环；两个shift使用本机默认。',
    ('只改变shift_video；恢复后只改变shift_audio', '分别改变对应模态的噪声时间映射；输出时长/分辨率保持，不保证某方向画面更清晰或声音更好。', '保存音画两路及5个配对seed；若可探针则记录对应sigma映射。'))

add('CreateCameraInfo', '不对称三维标尺：X/Y/Z方向有颜色标记；固定target=(0,0,0)、roll=0、zoom=1，透视相机。',
    ('fov=35 → 70度', '同一相机位置下视野扩大，物体投影通常变小；世界坐标/几何不变。', '固定RenderMesh/RenderSplat，测物体像素包围框。'),
    ('zoom=1 → 2；fov恢复35', '画面放大，物体可能被裁出画布；相机位置保持。', '记录camera_info与角标位置，不同时改distance。'),
    ('roll=0 → 90度', '画面绕视线轴旋转；不是物体绕世界Y轴转。', '检查Y-up和右手系；截图保存坐标轴。'))
add('Load3D|Load3DAdvanced|Preview3D|Preview3DAdvanced|Save3DAdvanced|SaveGLB', 'G1：已知2×1×1米非对称长方体，+X端红，+Y向上；纹理版另带UV。',
    ('加载/预览/保存后回读', '边界尺寸比例2:1:1、朝向与颜色标记对应；保存格式支持的材质/动画应保留。预览成功不等于已持久保存。', '用独立GLB查看器或3D软件查单位、bounds、mesh/animation数。'),
    ('有width/height的节点只改视口512×512→1024×512', '预览画布变化；模型世界坐标和尺度不应改变。只有filename_prefix时改前缀，模型内容应保持。', '避免自动取景掩盖尺度问题；SaveGLB没有视口尺寸则不做该变化。'))
add('MeshToFile3D', '单个带UV、棋盘贴图、顶点颜色的MESH；用GetMeshInfo记录顶点/面数。',
    ('MESH→FILE_3D_GLB→保存回读', '几何形状、UV布局、支持的材质属性可读取；必须真正落盘后检查GLB。', '统计面数/包围盒；顶点数可能因GLTF拆点变化，按位置/拓扑等价判断。'),
    ('仅换一张纯红base_color贴图', '几何保持，回读材质变红。', '不把材质丢失误判为几何转换成功。'))
add('GetMeshInfo', '已知单个三角形mesh：3顶点、1面；另备两个不重合三角形。',
    ('一个 → 合并两个三角形', '报告顶点/面数应从3/1变为6/2（未焊接）；MESH直通几何不变。', '文本输出接PreviewAny；检查实际报告包含哪些字段。'))
add('MergeMeshes', '两个不重叠三角形A、B，各3顶点1面。',
    ('仅A → A+B', '合并后6顶点2面；B面索引应正确偏移，不能连接到A的顶点。', 'GetMeshInfo和渲染，确认两个独立三角形。'),
    ('交换输入顺序', '整体空间几何保持，仅数组/面顺序可以变化。', '不要用文件字节一致判等。'))
add('DecimateMesh', 'G2：有2000面以上、轮廓非对称的网格；记录初始F0。',
    ('target_face_count=1000 → 500', '目标预算降低，面数通常下降；受算法/拓扑约束不保证恰好目标数。整体轮廓应可辨认，细节可能损失。', '记录实际F、F/F0、bounds和相同相机截图；不能只看速度。'),
    ('只切placement_mode', '目标预算不变；顶点位置/误差可能改变，不能预设哪种在每个网格都更好。', '比较薄片/孔洞/轮廓误差。'))
add('FillHoles', 'G2：已测周长的两个边界环，小孔0.1米、大孔1米；其它几何保持。',
    ('max_perimeter=0.2 → 2（本机范围内）', '前组只允许小孔填充；后组可同时填两孔。max_vertices需足够大，否则成为另一限制。', '检查边界环数、填充面法线和孔外顶点位置。'),
    ('fill_chains关闭→开启', '只在存在开放边界链的夹具上应出现分支差异；闭合孔素材不能验证该开关。', '分别保留闭环和开放链素材。'))
add('WeldVertices', '两个三角形共享边的位置，但使用重复顶点；复制位置完全相同。',
    ('小正epsilon_abs，epsilon_rel固定', '重复顶点被合并，面覆盖区域保持；顶点数下降。', 'GetMeshInfo；记录UV/颜色接缝是否受影响。'),
    ('两点距离跨越epsilon，逐步增大容差', '可能合并更多近邻；网格量化边界会影响结果，不能把阈值当欧氏球精确半径。', '同时记录坐标和格点；大容差导致细节塌陷属于风险观察。'))
add('RotateMesh', '非对称G1；mode=euler，动态子参数按界面XYZ；角度以度为单位。',
    ('绕Y=0 → 90度', '长轴从X方向转到Z方向，Y方向保持；顶点/面数不变。', '使用世界坐标检查，不让查看器自动旋转。'),
    ('绕同轴90度连续4次', '恢复原几何位置，允许浮点误差。', '顶点对应最大误差建议≤1e-5×场景尺度。'))
add('MeshSmoothNormals', '立方体：各面应有明确棱线；固定光照相机。',
    ('crease_angle小值→大值', '越过硬边判定阈值后，跨棱平滑法线增多；表面高光变圆滑，顶点位置不变。', '检查法线/渲染；不能以几何轮廓变圆作为正常预期。'))
add('RemeshMesh', 'G2，记录bounds、孔洞与连通块；其它参数默认。',
    ('resolution=默认 → 默认的下一档更高有效值', '距离场采样更细，通常保留更多细节且面数/耗时增加；不能保证严格面数关系。', '对比bounds、薄片是否保留、连通块数和耗时。'),
    ('project_back=false → true', '回投影应使重建表面更贴近原网格；不要求拓扑或顶点索引相同。', '对齐坐标后测表面距离。'))
add('RenderMesh|RenderSplat', 'G1或已知尺度S1，固定CreateCameraInfo和背景。',
    ('width=512,height=512 → width=1024,height=512', '输出IMAGE/MASK尺寸对应设定；三维数据本身不变。', 'GetImageSize，遮罩范围与物体投影对齐。'),
    ('只改background黑→白', '物体外背景改变；遮罩几何范围应基本保持。', 'MASK和RGB分别保存；透明边缘混色可变化。'))
add('PaintMesh|BakeTextureFromVoxel', '带红/蓝空间分区的voxel_colors；mesh横跨两区；Bake版本先UnwrapMesh。',
    ('交换体素红/蓝颜色', '对应表面区域颜色交换，几何位置保持；Bake输出按UV映射，不是屏幕投影。', '固定相机渲染，并检查贴图/顶点颜色。'),
    ('只增加纹理分辨率（Bake版本）', '贴图尺寸提高，色块边界可更细；没有UV时应阻止验收并补齐上游。', 'PaintMesh无texture_size则本项不适用。'))
add('UnwrapMesh|RenderUVAtlas', 'G1纹理版；Unwrap从无UV网格开始，RenderUVAtlas从有UV版本开始。',
    ('resolution=512 → 1024', 'UV图像尺寸相应变化；展开表面分片仍应覆盖模型。展开可能复制接缝顶点，但不应改变表面形状。', '查看UV岛、重叠与接缝；贴上棋盘格检查。'),
    ('Unwrap的padding增大', 'UV岛间距应增大，可能减少可用纹理面积；RenderUVAtlas没有padding，不执行此项。', '以实际像素间距计量，不只凭更稀疏印象。'))
add('ApplyTextureToMesh|MeshTextureToImage', '同一UV网格及红/蓝棋盘base_color；其它PBR贴图使用已知常量。',
    ('贴图附加后提取', '已附加的base_color内容/尺寸可恢复；未提供通道按节点的中性回退处理，不认定为提取失败。', '逐通道记录：base_color、metallic、roughness、occlusion、normal_map。'),
    ('base_color改为纯红', '只改变对应材质通道，几何/UV不变。', '提取像素和固定光照渲染双重检查。'))
add('BakeAmbientOcclusion', '有凹槽的高模与对应低模，低模已UV展开；先固定resolution=512。',
    ('strength低→高', '凹陷遮蔽通常增强，开放表面相对亮；结果不是深度图。', '在同一UV位置测凹槽/开放区域亮度。'),
    ('samples低→高', '随机采样噪声通常降低、耗时增加；不保证单次每像素更接近真值。', '固定其它参数，多次估计方差。'))
add('BakeNormalMapFromMesh', '带凸纹高模和对应低模，低模有UV；高低模同坐标尺度。',
    ('低模作为自己的high_poly → 带凸纹high_poly', '前组平面区接近中性法线色(0.5,0.5,1)，后组凸纹区出现方向颜色变化。', '使用glTF/OpenGL +Y解释，固定光照渲染检查凸凹方向。'),
    ('cage_distance从不足→覆盖高模偏移', '命中缺失区域应减少；过大距离可能误命中其他表面。', '记录未命中区域和伪影，不只比较更鲜艳。'))
add('SplatToFile3D|File3DToSplat|SaveGaussianSplat|PreviewGaussianSplat|PreviewPointCloud|SavePointCloud', '已知点数/尺度/颜色的S1或普通点云；严格区分Gaussian属性与普通XYZ点。',
    ('保存/序列化再回读，优先PLY', '位置/点数及格式支持的属性应保留；压缩格式允许量化误差。普通点云能加载不等于具有Gaussian尺度/旋转/SH。', '记录点数、bounds、属性字段、格式；相同相机比较。'),
    ('只改格式或保存前缀（实际存在的参数）', '前缀只影响路径；换格式可能损失高阶SH，须按格式能力记录，不要求渲染逐像素相同。', '比较同一视角及另一视角，避免漏掉视角相关颜色丢失。'))
add('GetSplatCount|MergeSplat', 'S1有N个Gaussian，S2有M个；先分别计数。',
    ('单S1 → 合并S1/S2', '计数N→N+M；合并是拼接，不自动做几何去重。', 'GetSplatCount读INT；重复合并S1两次应为2N。'))
add('TransformSplat', 'S1固定坐标；平移/旋转=0，scale各轴=1。',
    ('translate_x=0 → 1', '每个中心x增加1个场景单位，y/z不变；计数不变。', '检查中心数据和固定相机画面，不假定原单位必定米。'),
    ('均匀scale=1 → 2', '相对变换原点的中心距离和各Gaussian尺寸增加；不是仅渲染点大小变化。', '核对bounds和协方差/scale参数；非均匀缩放另测形状。'))
add('SplatToMesh', 'S1含清晰封闭主体和低opacity浮点；固定其余参数。',
    ('min_opacity低→高', '参与表面提取的低透明度Gaussian减少，浮散结构可能减少，也可能产生缺口。', '记录面数/连通块及主物体轮廓；不要求面数单调。'),
    ('resolution低→高', '采样网格更细，时间/内存通常增加；是否保留细节用固定近景比较。', '记录mesh bounds、面数、耗时。'))
add('DA3Inference|MoGeInference|MoGePanoramaInference', '固定带前景物与远处背景的照片；全景版本必须使用等距柱状全景。',
    ('推理后接对应Render与Mesh转换', '输出有限的几何数据；前景/背景应有可区分深度。不能未经标定宣称绝对米制深度准确。', '记录有效像素比例、深度范围、重建边界；全景检查接缝。'),
    ('resolution/resolution_level升一档', '细节采样和耗时/显存可能增加；遮挡处仍可能不可靠。', '固定相机与输入，对同一物体边缘检查。'))
add('DA3Render|MoGeRender', '冻结同一份geometry，避免每次重新推理。',
    ('output从depth换到本机支持的normal/confidence/sky', '显示对应不同数据通道；shape应与该几何地图匹配，不能把灰度深度当置信度。', '记录实际模式列表，并对已知天空/表面朝向区域解释。'))
add('DA3GeometryToMesh|MoGePointMapToMesh', '冻结同一geometry；batch_index选0；场景含前后景深度断层。',
    ('decimation提高', '采样更稀疏，顶点/面数通常减少；依据本机参数含义先确认是步长还是比例。', '读实际mesh统计；未确认方向前不签收。'),
    ('断层过滤由宽松变严格', '跨前后景的错误连接面应减少；可能增加边界孔洞。', '放大深度断层处，量边界环与跨层三角形。'))
add('MoGeGeometryToFOV', '冻结同一geometry及intrinsics。',
    ('unit=degree → radian（按菜单实际拼写）', '同一角度数值满足rad=deg×π/180；axis变化时应对应fx/width或fy/height。', '用2×atan(size/(2f))核对，先确认归一化内参尺度。'))
add('RTDETR_detect|SAM3_Detect', '照片含一人、一猫和空白背景；固定模型与图片。',
    ('threshold=0.3 → 0.7', '保留候选应更严格；若后处理也受阈值影响，不保证最终框数严格单调。', '记录类别、分数、bbox/Mask面积；同一候选分数不应因阈值本身随意变化。'),
    ('RTDETR class_name选person；SAM3使用person条件', '关注人目标，猫不应被当做人签收；模型漏检须如实记录。', '画框/叠mask，检查目标实际对应。'))
add('RemoveBackground', '前景清楚的人物图；另备纯背景负例。',
    ('人物图→纯背景', '人物图输出mask应覆盖主体；负例不应凭空出现同样人物形状。边缘发丝允许误差。', '用人工粗标注算前景/背景点正确率；透明输出和mask分别检查。'))
add('SAM3_VideoTrack|SAM3_TrackPreview|SAM3_TrackToMask', 'P4两人，A向左移动、B向右移动；保持模型、帧序列和跟踪结果。',
    ('object_indices选A → B（在TrackToMask）；Preview调opacity', 'Mask主体从A换B；opacity只改变叠加显示，不应修改跟踪ID或mask数据。', '逐帧叠加检查ID，交叉遮挡处记录身份切换。'),
    ('Track的max_objects=1 → 2', '允许跟踪对象上限增加；实际识别数≤上限，不承诺一定找到2人。', '逐帧统计有效ID；修改检测间隔单独计时/比较丢失帧。'))
add('SAM3DBody_Predict|SAM3DBody_Render', 'P3：单人24帧抬手侧移，固定相机；Predict使用同一模型，Render使用冻结pose_data。',
    ('Predict只切run_hand_refinement；Render只切render_style', '前者主要影响手部估计/耗时，不保证总误差下降；后者只改变表示，不应改变同帧动作阶段。', '逐帧看手腕/指尖及人物数量；不同节点不要同时改动。'),
    ('Render宽高512×512→1024×512', '输出尺寸改变，pose_data本身不变。', '通过GetImageSize验证；Predict无width参数则不做该项。'))
add('SAM3DBody_Smooth', '冻结24帧姿态，含静止段小幅抖动和一次明确抬手；保留原始数据。',
    ('strength=0 → 中间值 → 1（按本机范围）', '0应保留原始轨迹；增强平滑通常减小静止段相邻帧位置/旋转差，但可能引入滞后。', '计算静止段腕点一阶差分RMS；另外记录抬手峰值时刻偏移。'),
    ('只增大window', '时间邻域扩大；不能以动作幅度被抹掉当成平滑成功。', '同时检查抖动、峰值幅度、峰值延迟三项。'))
add('MediaPipeFaceLandmarker|MediaPipeFaceMeshVisualize|MediaPipeFaceMask|SAM3DBody_FaceExpression', '短片依次闭嘴→张嘴→眨眼；另一张无脸照片作负例。',
    ('目标区域/strength或绘制参数做单项变化', 'FaceMask选mouth只覆盖嘴区；Visualize只改颜色/粗细不改变landmark坐标；FaceExpression mouth_strength增强应主要影响嘴部驱动。', '固定同帧对照；Landmarker阈值变化记录检测数，不承诺全部帧命中。'),
    ('输入无脸帧，选择missing_frame_fallback（若存在）', '按fallback返回空/复用/错误中的实际约定；不能把上一帧复用误当本帧成功检测。', '记录原始检测标记与最终显示分开。'))
add('SDPoseKeypointExtractor|SDPoseDrawKeypoints|SDPoseFaceBBoxes', '人物全身照，另备两人照；先冻结keypoints。',
    ('Draw关闭draw_hands或提高score_threshold；FaceBBoxes增大scale', '手部开关只影响绘制；提高阈值减少低置信点显示；bbox的scale提高应扩展脸框而非移动脸中心。', '检查原keypoints不变；Extractor的预测误差用人工标注点衡量。'),
    ('Extractor单人→两人（正确提供bboxes）', '输出人数/关键点组应与有效检测输入对应；不能按可见骨架条数猜batch。', '逐人核对bbox、关键点与帧号。'))
add('FrameInterpolate', '两帧小球从x=64移动到x=128；固定interp_model。',
    ('multiplier=2 → 4', '每对原始帧间插入更多中间帧；常见保端点规则为(N-1)×m+1，先核对本机实际规则。', '数帧、检查首尾原帧及中间小球位置；模型可能有重影。'),
    ('两输入帧完全相同', '中间帧应接近原帧，不应产生大幅运动。', '计算差值并检查边缘。'))
add('ImageUpscaleWithModel|LTXVLatentUpsampler', '固定支持的upscale_model；IMAGE使用P1，LATENT使用匹配模型latent。',
    ('同一输入放大一次', '输出分辨率按模型倍率变化；输入图的角标/主要布局保持。模型可能新增或误造纹理，不以更真实为必过条件。', '从模型配置先读倍率s，验W_out≈sW_in、H_out≈sH_in；latent用其空间维度。'),
    ('纯灰图作为输入', '输出主体区域应仍近似均匀；记录边界/数值误差。', '对比输入/输出内部方差，不能因尺寸正确就忽略伪纹理。'))
add('LTXVConcatAVLatent|LTXVSeparateAVLatent', '已匹配的视频latent V与音频latent A，记录每路shape/dtype/值。',
    ('Concat→Separate', '恢复V和A两路，shape、dtype和samples数值保持；不是把音频帧当作视频通道拼接。', '直接比较张量，不能只看能采样。'),
    ('只改变A的长度，再组合', '视频路应保持；时长匹配约束是否报错按实际消费者检查。', '组合成功不等于时间轴同步。'))
add('VoxelToMesh|VoxelToMeshBasic', '标量体素场中只有一个闭合球，固定体素坐标和数值范围。',
    ('threshold取场内低/中/高三值', '等值面位置改变；方向取决于场是密度还是SDF，必须先明确场定义。若场f=r²，阈值增大球半径按sqrt阈值增大。', '用解析球场作诊断夹具；测bounds与面法线。'),
    ('阈值完全在场值范围之外', '无等值面，允许明确空结果或异常；不应返回上次球形网格。', '记录空网格处理。'))
add('GenerateTracks|WanMoveTracksFromCoords|WanMoveConcatTrack|WanMoveVisualizeTracks', '宽高512×384，24帧；单条轨迹从(64,96)到(448,288)；坐标来源节点用显式数组提供。',
    ('轨迹终点改成(64,288)', '可视化终点x应由448变为64；起点保持；帧索引与坐标对应。', '不经过扩散模型，先检查原始轨迹和叠加图。'),
    ('两条轨迹合并', '轨迹数量相加，不能把两条首尾串成一条；可视化颜色/粗细改变不应改坐标。', '读轨迹维度及首末坐标。'))
add('wanBlockSwap', '基础MODEL直接采样与经此节点采样两条支路，所有随机与条件相同。',
    ('旁路 → 经过该节点', '该内置占位实现是no-op，结果应保持；不应期待显存搬运优化。', '比较同环境输出与显存；不得套用同名第三方节点说明。'))

add('ImageCropToMask', 'P1与M1，设定输出256×192；M1包含中心白矩形。',
    ('只把mask白矩形平移64像素', '裁剪内容应跟随mask区域移动；最终尺寸仍由width/height决定。', '用原图坐标角标定位裁剪来源。'),
    ('pad_factor增大', '应包含更多mask外上下文，主体在固定输出画布中通常变小。', '固定grow_mask，防止两个扩区参数混淆。'))
add('ResizeImageMaskNode', 'P1或M1；resize_type展开后选明确宽高；width=256,height=192。',
    ('明确宽高 → 按倍数0.5（本机对应分支）', '对512×384输入，两种设置应同得256×192；最近邻下二值mask仍只有0/1。', '记录动态子字段名和值，不只保存顶层resize_type。'),
    ('mask插值最近邻→双线性', '边界可出现0到1之间灰值，尺寸不变。', '统计唯一值和边缘剖面。'))
add('ImageScaleToTotalPixels', 'P1；resolution_steps使用本机默认并记录。',
    ('megapixels=0.25 → 1', '输出面积接近25万→100万，宽高约各翻倍；取整使面积非精确目标。', '记录W/H、W×H与取整倍数；不要断言精确尺寸。'))
add('ImageRGBToYUV|ImageYUVToRGB', 'RGB灰阶渐变与四色P1；将RGBToYUV实际三个输出对应接回YUVToRGB的Y/U/V。',
    ('往返转换', '恢复原RGB，允许浮点误差；通道不得接反。', '张量最大误差建议≤1e-5，PNG回读允许1/255。'),
    ('只替换U或V为常量', '亮度Y保持，但颜色发生变化；输出尺寸不变。', '记录采用的YUV偏移/范围，不能假定所有标准U/V中性值相同。'))
add('Morphology', '黑底白色矩形，kernel_size=3。',
    ('operation=dilate → erode（本机对应枚举）', '白区分别扩大/收缩；3×3核时矩形直边通常各移动1像素。', '量白区bbox，边界外充分留黑。'),
    ('kernel_size=3 → 5', '对同一操作影响范围扩大；不要输入偶数核后猜如何取整。', '记录核形状与实际枚举。'))
add('ImageColorToMask', 'P1纯红/绿/蓝/白角标；color=0xFF0000。',
    ('color红 → 绿', '仅对应颜色区域成为白色mask，其它纯色块为黑。', '用无压缩PNG；JPEG噪声会影响精确颜色匹配。'))
add('MaskPreview', 'SolidMask依次0、0.5、1。',
    ('输入三种值', '预览黑、灰、白；不产生持久output文件作为保存结果。', '截图并核对同尺寸。'))
add('PorterDuffImageComposite', '红色source与蓝色destination；使用明确已核对的alpha约定，先双方全不透明。',
    ('mode=source-over，源alpha全不透明→全透明', '输出从源红色切换到目标蓝色；0.5时按合成alpha公式混色。', '先以Split/Join往返校准遮罩是否反alpha；记录输出颜色与alpha。'),
    ('交换source/destination', '不透明source-over结果跟随新source；表明顺序不可交换。', '不要把Porter-Duff mode当普通blend_mode。'))
add('PrimitiveBoundingBox|CreateBoundingBoxes|DrawBBoxes|CropByBBoxes|LayersFromBoundingBoxes', 'P1；框x=128,y=96,width=256,height=192；交互编辑器绘制同一矩形。',
    ('框x=128 → 192，其它不变', '框整体右移64；裁剪内容或图层位置跟随改变，不能只改预览而输出坐标不变。', '读取bbox并叠加；Crop的输出尺寸由output_width/height决定。'),
    ('一个框 → 两个框（Primitive使用两个实例）', '绘制/裁剪/图层消费者应处理两区域，保留顺序与对应关系。', '分别在框内放红/蓝标记以确认配对。'))
add('AddLayer|ImageCompositor', '512×384蓝底，上叠128×128红层，位置(64,64)，normal模式。',
    ('红层opacity=0 → 0.5 → 1', '区域内为蓝→红蓝混合→红；区域外蓝底不变。', '读取最终合成IMAGE的内外像素。'),
    ('x增加64；再单独调整z_index', '层右移64；层次顺序只在存在重叠层时改变遮挡。', '不要同时变位置/透明度。'))
add('Painter|WebcamCapture', '固定画布512×384；Painter画一个红点，Webcam对准带红/蓝角标的纸。',
    ('Painter移动红点；Webcam更换纸面内容后再次采集', '输出内容跟随实际画布/摄像头改变，尺寸按设置；不能仍是旧缓存图。', '输入前端组件不是普通文件路径；检查浏览器授权和队列采集开关。'),
    ('只改width/height', '输出尺寸按设置改变；前端缩放/裁剪行为需记录。', '用GetImageSize核对，权限失败标阻塞。'))
add('SaveImageAdvanced', 'P1与P2透明图；先PNG。',
    ('PNG保存回读', '尺寸和RGB像素按8bit量化保持；透明图检查alpha是否支持并保留。', '比较解码像素，忽略元数据和文件字节差异。'),
    ('format切本机支持的JPEG分支', '有损编码可能改变像素；透明通道不应被当作必然保留。记录quality子参数，比较MAE/文件大小。', '同输入、同尺寸；quality更高不保证所有短文件大小严格单调。'))
add('SaveSVGNode', '需要真实SVG类型上游；本项目索引中缺少独立生产节点，先标BLOCKED_INPUT，不用STRING冒充。',
    ('取得合法SVG输入：10×10红矩形后保存', '文件能被SVG解析器/浏览器渲染为红矩形，尺寸/viewBox一致。', '保存前记录SVG对象来源；无法取得时不可标通过。'),
    ('矩形fill红→蓝，或仅改filename_prefix', '改fill改变渲染颜色；改前缀仅改路径。', '先解开输入阻塞，再执行。'))
add('LoadImageDataSetFromFolder|LoadImageTextDataSetFromFolder|SaveImageDataSetToFolder|SaveImageTextDataSetToFolder|LoadVideoDataSetFromFolder|LoadVideoTextDataSetFromFolder', '准备3个唯一文件a,b,c；每个内容显示自身编号；caption分别为ID:a/ID:b/ID:c，同主文件名。',
    ('读取或保存回读', '样本数3；带文本节点的图文/视频文本按主文件名保持对应。不能假设操作系统列目录顺序就是语义顺序。', '建立编号→caption映射比较；记录输出是list还是batch。'),
    ('新增d及其caption；另做单个caption缺失负例', '完整数据变4项；缺失caption按实现报错/空文本/跳过之一，必须明确记录，不能静默错配到下一项。', '缺失分支在源码未核对前标探索；保存模式只在临时目录测试。'))
add('ShuffleDataset|ShuffleImageTextDataset|ShuffleVideoDataset|ShuffleVideoTextDataset', '5个编号0..4样本；有文本的节点各配相同编号caption。',
    ('seed=123重复两次；再124', '同seed次序可复现；不同seed允许偶然同排列；样本集合和数量不变。', '比较顺序列表和多重集合。'),
    ('带caption版本检查每项', '无论次序如何，图片/视频编号和caption编号必须匹配。', '错配一次即FAIL，不用随机性解释。'))
add('GLSLShader', '按本机shader模板读取输入纹理，先写恒等shader；P1输入。',
    ('恒等 → RGB取1-原值，保留alpha', '恒等应保留P1；反相shader产生互补颜色；画布大小由size_mode决定。', '取角标RGB；纹理坐标上下方向先用TOP校准。'),
    ('故意写语法错误', '应产生编译错误信息，不应把旧输出当作本轮成功。', '保留编译日志并恢复shader。'))
add('SetLatentNoiseMask|VAEEncodeForInpaint|InpaintModelConditioning', '固定P1、匹配VAE与inpaint模型；mask先全0再中央白矩形M1；保持seed。',
    ('mask全0 → M1 → 全1', '限制区域从无到中央再到全图；实际变化受采样器/模型影响。VAEEncodeForInpaint还会预处理白区，不能只看重绘图猜mask正确性。', '先检查latent noise_mask/编码输入，再看解码结果；VAE会造成区域外微差。'),
    ('grow_mask_by增大（仅该参数存在的节点）', '噪声/填充作用边界扩展；画布尺寸不变。', '可视化mask bbox，不要求生成内容严格止于单像素边界。'))
add('LatentComposite|LatentCrop|LatentUpscale|LatentUpscaleBy', 'SD1.5 latent来自512×384 P1；samples=[1,4,48,64]，固定相同VAE。',
    ('Crop选256×192；Upscale目标1024×768或scale_by=2；Composite移x=64', 'Crop空间维为24×32；Upscale为96×128；Composite按8倍像素换算平移8个latent单元。只对实际节点执行对应操作。', '先查张量shape和位置，再解码；其它模型压缩率不能套8。'),
    ('恒等尺寸/零位移与原始latent对照', '不需要变化的区域/维度应保持；插值/羽化仍按所选方式计算。', '记录每个LATENT字段，避免丢noise_mask。'))
add('LatentConcat|LatentCut|LatentCutToBatch', '可控诊断latent，每个切片填自身编号；维度长度均已记录。',
    ('Concat沿选定dim合并长度2与3', '对应维度长度变5，其余维度保持；不能沿不匹配维度拼接。', '检查shape及切片编号0..4。'),
    ('Cut index=1,amount=2；CutToBatch slice_size=1', 'Cut取所选轴两个切片；CutToBatch将所选轴的切片转到batch，顺序保持。', '必须先确认dim枚举对应B/C/T/H/W，不能凭名称猜轴。'))
add('LatentBatchSeedBehavior', '包含重复图像latent的batch，固定同一采样链与seed。',
    ('切换seed_behavior的实际两种选项', '应改变batch索引与噪声种子的对应方式；图像latent值不应凭空改变。', '先查batch_index元数据，再比较各帧生成结果；记录枚举实际含义。'))
add('LatentApplyOperation|LatentApplyOperationCFG|LatentOperationSharpen|LatentOperationTonemapReinhard', '固定latent或MODEL，搭配对应LATENT_OPERATION；先旁路取得基准。',
    ('构造operation并实际接入消费者', 'Operation对象本身不是处理后的latent；普通Apply改变latent，CFG版本影响采样过程中的预测。', '在真正执行位置查samples，不能用对象字符串当处理成功。'),
    ('锐化alpha/tonemap multiplier使用小幅有效变化', '数值分布/局部对比会变化，shape保持；不保证解码图主观更好。', '记录min/max/mean/std及固定seed结果；具体公式按operation源码核对。'))
add('ConditioningAverage|ConditioningCombine|ConditioningConcat|ConditioningMultiply|ConditioningZeroOut', '两份同模型条件A=red cube、B=blue sphere；保留metadata和embedding shape。',
    ('执行对应操作', 'Combine增加条件条目；Concat拼接token/序列；Multiply缩放embedding；ZeroOut清零指定条件内容；不能互相当作等价加法。', '查条目数、tensor形状/统计与metadata，生成图片只作辅助。'),
    ('Average权重0/1；Multiply系数0/1；Combine/Concat的A,B交换', 'Average端点回到对应条件；Multiply为零/原值；交换合并顺序需记录顺序变化，不能保证生成结果不变。', '准确端点方向以conditioning_to_strength名称及源码确认。'))
add('ConditioningSetArea|ConditioningSetAreaPercentage|ConditioningSetAreaPercentageVideo|ConditioningSetMask|ConditioningSetAreaStrength', '左半区域条件red cube，右半blue sphere；同一基础模型/latent/seed。',
    ('区域从左半移到右半；或mask左右互换', '条件metadata中的区域必须随之改变；生成对象更倾向于指定区域，但不承诺边界绝不泄漏。', '先检查area/mask元数据；再5seed测目标中心是否落在指定半区。'),
    ('strength=0 → 1', '0应去掉该区域条件贡献，1恢复设定权重；尺寸/整体时长不变。', '用仍有全局条件的基线，避免所有条件关闭导致无效输入。'))
add('ConditioningTimestepsRange|ConditioningSetTimestepRange|CFGOverride', '固定20步采样；记录每步sigma/percent；选择0.25..0.75有效区间。',
    ('区间0..1 → 0.25..0.75', '作用只限中间噪声区间；百分比不等于简单step/20，须按模型sigma映射判定。', '检查条件/CFG实际生效日志或探针；最终图片无法定位每一步。'),
    ('互不相交的两个区间', '每个区间分别生效，不应把全程效果误当时间控制正确。', '记录采样轨迹和参数，不假定起止端点是否包含。'))
add('ManualSigmas|FlipSigmas|SetFirstSigma|SplitSigmas|SplitSigmasDenoise|ExtendIntermediateSigmas|SamplingPercentToSigma', '诊断SIGMAS=[4,2,1,0]，仅检查序列，不直接拿不匹配sigma喂真实模型。',
    ('Manual输入该列表；SetFirstSigma改为8；Split step=2', 'Manual应给4项；SetFirst仅首项变8；Split两段共享切分边界时应可重建原序列（去掉重复边界）。', '数值探针逐项记录；共享边界规则先按实际实现核对。'),
    ('Flip反转；Extend插入点；Percent 0→1；SplitDenoise改变比例', '分别改变顺序/中间点数/模型噪声映射/切分位置；Flip可能将零替成小正值，不能要求字面严格逆序。', '先写出本机输出序列，再对照源码签收；不以能生成图片代替序列验证。'))
add('KSamplerSelect', '固定同一SIGMAS、NOISE、Guider和latent。',
    ('sampler_name=euler → heun（本机均支持时）', 'SAMPLER对象改变，最终shape不变；heun通常增加模型求值次数，质量不保证更好。', '实际接SamplerCustomAdvanced；计模型求值和耗时，不只看对象名称。'))
add('CreateHookKeyframe|CreateHookKeyframesInterpolated|CreateHookKeyframesFromFloats|SetHookKeyframes', '已有兼容LoRA hook；开始0、结束1；建立强度从0到1的时间表。FLOATS来源缺失时先标BLOCKED_INPUT。',
    ('关键帧数2 → 3，采用线性插值', '开始/结束强度不变；中间新增一项，线性中点强度0.5，时间percent=0.5。', 'print_keyframes可用时开启；不靠最终图片猜插值表。'),
    ('固定时间表，只改strength_mult或端点强度', '对应时段hook强度随之改变；SetHookKeyframes负责绑定，不应再生成新的LoRA权重文件。', '逐关键帧打印，再小步采样核对生效。'))
add('CombineHooks2|CombineHooks4|CombineHooks8', '两个明确不同的hook A/B；分别只有一个可观察的权重增量。',
    ('A → A+B', '合并后包含两组hook；顺序/冲突按实现处理，不能只看HOOKS对象存在就验收。', '检查hook列表标识及采样时是否都生效。'),
    ('交换输入或重复A', '记录去重/叠加规则，未确认前不承诺同一hook重复两倍。', '此冲突分支为探索项；保存对象摘要与日志。'))
add('TrainLoraNode', '3张自有小图+同一标识caption；匹配模型；固定训练seed；先steps=2确认闭环，再做10/20步小实验。',
    ('steps=10 → 20，固定其它参数', '应产生对应更新步数的LoRA和有限loss序列；训练loss不保证逐步下降。', '记录实际optimizer step、loss、耗时、显存；加载LoRA比较固定验证集。'),
    ('learning_rate小值→2倍小值', '参数更新尺度通常增加，但可能震荡/过拟合；若出现NaN则FAIL而非更强效果。', '同初始权重重新开始两次，不能从10步结果继续冒充独立20步实验。'),
    ('训练LoRA以strength=0与1加载', '0应近似基模；1应可运行，是否学到标识用未见验证图/提示词评价。', '训练集改善与验证泛化分别记录；保存模型与配置hash。'))
add('MakeTrainingDataset|ResolutionBucket|SaveTrainingDataset|LoadTrainingDataset|LossGraphNode', '3个样本，两个同分辨率、一个不同分辨率；caption带唯一ID；loss夹具=[1.0,0.8,0.9]。',
    ('编码→按分辨率分桶→保存回读', '总样本数仍3，分桶2+1，caption与latent配对保持；回读shape/dtype/精度符合存储格式。', '记录每桶ID与shape；不能只检查文件存在。'),
    ('LossGraph绘制给定三点；SaveTrainingDataset改shard_size', '曲线有先降后升三个点；分片大小变化只改文件划分，不应丢样本或改标签。', '分别核对曲线坐标与合并后的数据多重集合。'))

add('LTXVDurationPredictor', '匹配模型及duration_head；短提示词描述一个简单动作；固定frame_rate。',
    ('min_seconds/max_seconds使用合法的2..6秒范围', '返回时长应落在约束范围，并按模型合法帧网格对齐；语义预测值不是任意正整数帧。', '检查返回时长/帧数与模型网格；边界取整可能需单独解释。'),
    ('只缩小max_seconds', '预测最终时长不应超过新的有效上限（网格取整按实现）；不能由此判断自然动作一定能完成。', '记录原始预测与截断后结果，若仅暴露后者则标明。'))
add('GetICLoRAParameters', '已加载含IC-LoRA metadata的真实LoRA模型；另备普通LoRA作负例。',
    ('IC-LoRA → 普通LoRA', '前者返回可供LTXVAddGuide使用的参考参数；后者缺字段时应明确缺省/错误，不能沿用旧IC参数。', '打印元数据字段和值，并与safetensors header核对。'))
add('VOIDQuadmaskPreprocess', '二值mask中央矩形，边缘远离画布；dilate_width先默认。',
    ('dilate_width增大', '膨胀/边界区域变宽，输出quadmask编码分区应可区分；不能将quadmask直接当普通0/1 mask。', '记录实际离散值集合及各区域面积，再与源码的四区定义核对。'))
add('SeedVR2Preprocess|SeedVR2PostProcessing', '带alpha的非整倍数尺寸图；保存original_resized_images。',
    ('Preprocess→匹配处理→PostProcessing', '预处理补齐模型要求的边界并去掉alpha；后处理恢复目标范围/alpha；不能拿预处理图直接当最终RGBA。', '记录每步W/H/C及最终alpha，与原图对应。'),
    ('只切color_correction_method（PostProcessing）', '色彩统计可能变化，最终几何尺寸/alpha范围保持。', '固定同一生成图，比RGB统计与边缘位置。'))
add('WanDancerPadKeyframes|WanDancerPadKeyframesList', '少量编号关键帧及固定音频；segment_length按合法默认。',
    ('segment_index=0 → 1；List版本num_segments=1 → 2', '单段选取位置变化；List应产生相应段数，每段关键帧/音频时间对应。', '读每段编号和长度；padding重复帧须记录来源。'),
    ('关键帧不足一段', '应按实现补齐或明确报错，不能静默错位音频；具体补法未核实前为探索项。', '检查每个输出段首尾编号、音频起点。'))
add('SetUnionControlNetType', 'Union ControlNet模型；一张真正的边缘控制图与一张深度图。',
    ('type选择边缘→深度，并分别配对应控制图', '控制类型元数据切换；下游应按所选任务使用控制图。两次同时换type和图用于兼容性验证，不用于因果归因。', '打印控制类型ID，固定其余采样条件。'),
    ('图固定，仅切type', '输出可能明显变化或退化，不能把类型错配当模型质量问题。', '用正确配对作基准，记录构图一致性。'))
add('FluxKontextImageScale', '512×384和384×512两张方向相反的P1。',
    ('横图 → 竖图', '输出尺寸按Kontext目标面积/网格规则调整，方向与近似长宽比应保留；不是固定放大倍率。', 'GetImageSize记录W/H与面积，核对源码目标网格后判定。'))
add('TripoSplatPreprocessImage', 'P1及中央物体mask；物体占画布一半，黑背景。',
    ('size默认→较小合法值', '输出正方形画布边长按size变化；主体居中且保留边距。', '量shape、主体bbox和背景像素。'),
    ('erode_radius增大', 'mask边缘向内收缩，可能削去边缘杂色，也可能损失薄结构。', '输入mask与输出主体边界对照。'))
add('WanCameraEmbedding', 'width=512,height=384，合法length；相机动作先选静止/最小运动配置。',
    ('只改变speed，保持camera_pose', '相机轨迹变化幅度/速度按该pose模式变化；embedding时间长度保持。', '优先解读相机轨迹/矩阵；最终视频运动只是统计观察。'),
    ('只改fx或fy', '内参对应轴焦距变化；不能解释为相机世界位置平移。', '记录内参单位/归一化定义及embedding shape。'))
add('SCAIL2ColoredMask', '两个人的driving_track_data，必要时有对应ref_track_data。',
    ('object_indices选0 → 1 → 两者', '目标mask分别对应不同的人及两者；颜色编码应与所选sort_by/replacement_mode一致。', '在同帧与原视频叠加，检查ID与颜色对应而非只看彩色图。'),
    ('切replacement_mode', '替换规则改变，不应偷偷交换错误人物；缺少参考track时按分支依赖记录阻塞。', '保存输入ID映射和输出色值。'))
add('TripoSplatSamplingPreview', '已跑通TripoSplat采样；同模型、VAE、seed，固定最终解码。',
    ('启用预览；只改yaw/pitch', '采样时预览视角变化，最终latent的采样目标不应因查看角度而变化。', '比较最终latent；排除随机解码预览的seed影响。'),
    ('num_gaussians低→高', '每步预览的Gaussian数量/开销改变；不是必然提高最终输出质量。', '计预览时间与点数，最终解码数量参数单独固定。'))
add('LTXVPreprocess', 'P1细线与渐变图；img_compression使用本机支持的基准。',
    ('压缩较弱→较强', '预处理图可能出现压缩失真，尺寸保持；参数方向先查本机范围（质量数字可能与压缩程度相反）。', '比较边缘块效应、MAE，不直接把参数更大解释为失真更大。'))
add('LTXVConditioning|ConditioningStableAudio', '固定positive/negative，LTXV frame_rate=24；StableAudio seconds_start=0,seconds_total=2。',
    ('frame_rate=24 → 12；或seconds_total=2 → 4', '对应时间条件元数据改变；本节点不直接插帧/重采样音频。', '查看CONDITIONING的时间字段，再用匹配模型生成；不得把条件FPS与容器FPS混为一谈。'))
add('LTXVAddGuide|LTXVImgToVideoInplace|LTXVCropGuides', 'LTX匹配latent和VAE；参考为明显红色首帧；固定条件。',
    ('AddGuide的frame_idx从开头移到合法中间帧；Inplace切bypass；Crop前后比较', '锚点应移动到对应位置；bypass应跳过注入；Crop应移除引导占用的相应部分。三种操作分别检查输出端口，不能混接。', '查latent shape/condition引用帧；生成帧符合程度另作5seed统计。'),
    ('引导强度从低到高（仅存在strength时）', '引导约束增加，但不保证画面逐像素等于参考；保持输出时长/分辨率。', '比较目标帧邻域和参考图，记录伪影。'))
add('LTXVReferenceAudio|ReferenceTimbreAudio', '同一句话的两种合法自有声音参考A/B；同提示词、同随机条件。',
    ('参考A → B', '参考音色/身份条件应改变；生成声音可能更接近对应参考，文本内容和时长不应由引用路径错误改变。', '先确认音频latent/条件字段改变；再盲听与说话人相似度评估，不能保证准确克隆。'),
    ('身份引导强度低→高（若存在）', '身份倾向可能增强，质量不保证单调；记录失真和可懂度。', '5seed配对，使用同一段文本和参考时长。'))
add('VAEDecodeAudio|VAEDecodeAudioTiled|VAEEncodeAudio|LTXVAudioVAEDecode|LTXVAudioVAEEncode', '匹配的audio VAE；A1=1秒440Hz低幅正弦；先Encode→Decode。',
    ('基准往返；再音频时长翻倍', '输出音频的采样率/通道符合VAE配置，时长按模型网格可能补齐；主频应接近440Hz。时长翻倍对应latent时间轴增长。', '记录输入/输出样本数、频谱、RMS；VAE有损不要求逐样本相等。'),
    ('Tiled节点只改tile_size/overlap（一次一项）', '整体时长/声道应保持；接缝噪声、显存和时间可能改变。普通节点无该参数则用重复基准对照。', '检查拼接时刻附近波形跳变，不只听整段。'))
add('TrimVideoLatent|ReplaceVideoLatentFrames|SeedVR2TemporalChunk|SeedVR2TemporalMerge', '诊断latent的每个时间片填不同编号；SeedVR2用匹配格式与固定重叠量。',
    ('Trim裁掉已知数量；Replace在index放入两个新编号片；Chunk→Merge', '裁剪减少时间片；替换只改变选定时间区间；分块再合并恢复时间顺序与总长度（重叠融合区按权重计算）。', '先查张量编号而非解码画面；确认trim_amount单位为latent片还是输出帧后计算。'),
    ('仅增加temporal_overlap（若存在）', '重复覆盖区域扩大；最终时间长度不应因把重叠重复计算而变长。', '核对Hann交叉淡化区域，恒定值输入应在融合后保持恒定。'))
add('NormalizeVideoLatentStart', '构造首段均值偏高、后段均值正常的同方差latent；保留各段统计。',
    ('start_frame_count增加', '被标准化的前缀区间扩大；区间之外不应被同样改写。', '逐时间片比较均值/std；参考段std=0需单独处理。'),
    ('reference_frame_count改变', '目标统计由新的参考区间决定；不能保证生成视频闪烁必然降低。', '先验证统计转换，再观察视觉效果。'))
add('Hunyuan3Dv2ConditioningMultiView|SV3D_Conditioning|StableZero123_Conditioning|StableZero123_Conditioning_Batched|Pixal3DConditioning', '非对称对象参考图，正面有红标；固定模型与seed。',
    ('切换视角条件：azimuth/elevation/camera_angle_x中实际存在项；多视图版本交换front/back', '相机条件或视图身份应改变；生成更倾向目标观察方向，不保证精确几何重建。', '先查条件字段；用红标判断前后侧，不以主观旋转感判定。'),
    ('Batched版本增加azimuth_batch_increment', '批内目标视角间隔增加；图片数量由batch_size决定，不由角度步长决定。', '逐张记录角度与结果对应；其它节点此参数不存在不做。'))
add('TextGenerate|TextGenerateLTX2Prompt', '匹配支持文本生成的CLIP/语言模型；prompt要求仅输出一句含red cube的英文描述。',
    ('max_length低→高，固定sampling_mode', '允许生成的token预算提高，但遇到结束符可能提前结束；字符长度不等于token数。', '记录生成token数、停止原因和返回文本；不能保证更长更好。'),
    ('确定性解码重复；再启用随机采样', '确定性模式同环境应复现；随机模式可能变化，若无seed则不可要求逐字一致。', 'use_default_template/thinking保持固定；不得同时换模板。'))

add('MiniMaxH3ReferenceToVideo', '匹配H3模型、CLIP、video VAE、audio VAE；1344×768,length=124；一张高分辨率人物参考；prompt明确引用<Picture 1>，固定seed。',
    ('同一ref_image_1换成另一人物，标签不变', 'minimax_refs中图像参考块更新；生成主体身份倾向相应改变。输出positive和AV latent，没有负向条件输出。', '先查参考块数量/类型，再5seed盲评主体特征；不能承诺身份绝对一致。'),
    ('ref_image_size=match → max', '高分辨率参考可能保留更大尺寸/更多token，耗时和显存可能上升；小图可能两种模式相同，因为不会任意上采样。', '记录参考resize后宽高与token/latent网格；不要用小参考图验证两档差别。'),
    ('reference video依次4、5、21、22帧，输出length至少22', '已核对版本：4帧报错；5合法；21裁到5；22保留22。参考视频按17k+5向下裁，区别于输出时长向上对齐。', '先检查编码前帧数；参考视频期望24fps。不要只看最终视频时长。'),
    ('视频参考附带同编号ref_video_audio_N，然后另接独立ref_audio', '视频音轨通过同编号配对；音频标签按呈现顺序独立编号，不能把Video编号直接等同Audio编号。', '记录参考顺序/标签、音频采样率转换和metadata块kind。'))
add('MiniMaxH3ImageToVideo', '同一H3链路；first_frame=P1；last_frame为布局明显不同的蓝图；length=124，width/height固定。',
    ('只接first_frame → 同时接last_frame', '条件中末帧引导增加；生成末段更趋近末帧参考，不能要求整段逐像素插值。', '查首末引导metadata与视频00/中/末帧，5seed记录首末符合度。'),
    ('length=124 → 141，其它保持', '输出名义时长从124/24变141/24秒；首末参考仍在相应端点，运动速度/路径可能改变。', '解码数帧、查FPS，不仅看播放器四舍五入的秒数。'))
add('BasicScheduler', '匹配MODEL，固定scheduler；steps=20,denoise=1。',
    ('steps=10 → 20，denoise=1', '常规输出SIGMAS长度11→21；每个值有限；终止项按所选scheduler约定。', '逐项导出，不用采样器进度条代替。'),
    ('steps=20，denoise=0.5', '先按int(20/0.5)=40步生成完整时间表，再截最后21项。可与40步denoise=1的尾部做精确对照。', '对比两个SIGMAS数组。'),
    ('denoise=0', '已核对版本返回空SIGMAS，不是21个零。', '此项仅检查调度器，空数组不一定可直接喂所有采样器。'))
add('KarrasScheduler', '仅检查序列：steps=3,sigma_max=4,sigma_min=1,rho=1，不直接采样真实模型。',
    ('rho=1运行', 'Karras公式退化为线性，预期[4,2.5,1,0]（末尾附零）。', '数值探针逐项核对；容差1e-6。'),
    ('rho=2，其它不变', '按幂插值预期[4,2.25,1,0]；首尾非零sigma不变，中间点改变。', '公式：(max^(1/rho)+u×(min^(1/rho)-max^(1/rho)))^rho；u=0,0.5,1。'))
add('LoraLoaderBypassModelOnly|LoraLoaderBypass|LoraModelLoader', '兼容LoRA；固定基模型/seed/条件；LoraModelLoader使用训练产出的LORA_MODEL。Bypass在这里是前向计算注入策略，不是禁用LoRA；命名带Bypass的两个节点并没有bypass开关输入。',
    ('普通权重合并路径 → bypass前向注入路径，保持相同非零LoRA强度', '两条路径都应应用LoRA；在相同支持实现/精度下结果应接近，原始基权重与前向额外运算的存在方式不同。', '读取原始权重/前向注入配置；量输出误差，不能以“无LoRA”为bypass预期。'),
    ('strength_model或实际strength参数=0→1；其余文本强度固定', '0移除对应增量，1应用LoRA增量；外观不保证单调改善。LoraModelLoader的bypass_mode若存在，切换的是应用策略。', '固定5seed及触发词，记录匹配权重数和下游误差。'))
