"""Maintain task scenarios and conservative, port-aware upstream examples.

The fixed index proves interfaces, not family compatibility. Unreviewed matches
remain explicitly labelled candidates, never promoted to mandatory edges.
"""
import re

# Each line follows data/experiments.json node order. Every operation is authored;
# count assertions prevent silently attaching an operation to the wrong node.
OPERATIONS = {
'A01': '用滑块对照处理前后的两张图|读取图片宽高和批次数|把本地图片读入工作流|重新使用输出目录中的图片|在画布直接检查图像|将结果保存为图片|把中间值转成可读文本检查',
'A02': '将颜色转为整数通道值|在数字类型之间转换|组织动态类型的输入列表|编辑供下游使用的数值曲线|把可选项集中为下拉选择|用表达式计算宽高或其他参数|从分辨率选项得到尺寸|集中管理随机种子|集中提供布尔开关|集中提供小数参数|集中提供整数参数|让多个下游共用一段文本|维护多行提示词或文本',
'A03': '在文本前添加固定说明|在文本后添加风格词|构建 Ideogram 所需的结构化提示|比较两段文本|判断文本是否含目标片段|连接多段文本|将数组转换为文本|将字典转换为文本|统一文本大小写格式|将文本转为小写|将文本转为大写|在图像上叠加说明文字|按正则提取目标字段|从 JSON 提取字符串|用模板填入动态文本|用正则判断输入是否符合格式|合并多份文本列表|替换文本中的目标片段|执行指定文本替换|按正则批量替换文本|保存生成文本或标签|清理多余空白|截取指定文本区间|统计文本长度|修剪文本边界|将文本限制到所需长度',
'A04': '合并必须同时成立的布尔条件|按选择条件切换数据分支|反转布尔条件|合并任一成立即可的布尔条件',
'A05': '按新版裁剪接口取图像区域|从中心裁剪构图|按坐标裁剪图像|随机裁剪训练或测试样本|按遮罩范围裁剪图像|翻转图像方向|为局部重绘扩展图像画布|缩放并填充到目标画布|对图像或遮罩统一调整尺寸|按长边统一图片尺寸|按短边统一图片尺寸|旋转图像|将图片拼接成组合画面|限制图片最大边长|按总像素预算调整图片尺寸|把图片缩放到指定宽高|按比例缩放图片',
'A06': '调亮或调暗图片|调整明暗反差|将 RGB 图像转为 YUV 表示|将 YUV 表示还原为 RGB|反转图像颜色|规范化图像数值分布|添加可控图像噪声|对图像结构执行形态学操作|混合两张图片|柔化细节或边界|提取边缘供观察或结构控制|减少图像颜色数量|增强边缘细节|迁移参考图的颜色特征|检查图像颜色与亮度分布',
'A07': '从文件读取指定通道作为遮罩|组织多张遮罩的批次|按运算组合遮罩|从指定颜色提取遮罩|将图像通道转换为遮罩|把遮罩转换成可预览图像|创建固定强度的矩形遮罩|裁剪遮罩区域|柔化遮罩边缘|扩张或收缩遮罩范围|交换遮罩选区与非选区|直接观察遮罩分布|将遮罩按阈值分成选中与未选中区域',
'A08': '按遮罩把前景合成到背景|把 RGB 与 alpha 遮罩合并|使用 Porter-Duff 规则合成透明图层|拆出图像颜色与 alpha 信息',
'A09': '组合多张图像为批次|拼接两个图像批次|去除相似或重复图片|从批次选取指定图片|制作批次结果的网格图|合并图像列表|将已处理图块拼回图像|重新组织图像批次大小|重复同一批图像供多组对照|将图片拆成图块列表',
'A10': '为图层集合添加一层|按图层布局合成图片|按边界框建立图层布局|在图片上标出边界框|按多个边界框提取局部图像|通过边界框编辑器组织多个区域|提供一个明确的边界框',
'A11': '创建纯色背景或测试画布|手绘输入图像|将帧序列保存为 APNG 动画|将帧序列保存为 WebP 动画|按高级选项保存图片|将已有 SVG 对象保存为文件|从摄像头采集图像',
'A12': '从文件夹批量读取图片|读取图片及配对文本|保存图像数据集|保存图像与文本配对数据集|打乱图像数据顺序|保持图文配对地打乱样本',
'A13': '用自定义 GLSL 片元程序实现图像效果',
'B01': '选择 CLIP 使用的输出层|把提示词编码成生成条件|调整 T5 分词填充选项|从 checkpoint 同时取得模型与编码组件|加载图像条件所需的 checkpoint 组件|按指定配置加载 checkpoint|单独加载文本编码器|加载一组双文本编码器|加载一组四文本编码器|加载一组三文本编码器|从 Diffusers 目录加载模型组件|单独加载扩散模型权重|单独加载 VAE 权重',
'B02': '将采样后的潜变量解码为图像|分块解码以控制显存占用|将输入图像编码为潜变量|分块编码大图以控制显存占用',
'B03': '为基础图像生成创建初始潜空间|将模型条件与潜变量送入一体化采样过程',
'B04': '控制加噪开关与采样起止阶段',
'B05': '为局部重绘整理图像遮罩和条件|限定潜变量中的加噪区域|把图像与遮罩编码为重绘输入',
'B06': '按比例混合两个潜变量|按位置拼接潜变量区域|用遮罩合成潜变量|回读保存的潜变量|保存中间潜变量供复用|按目标尺寸放大潜变量|按比例放大潜变量|将两个潜变量相加|调整潜变量批次的种子索引行为|沿指定维度连接潜变量|截取潜变量区间|将潜变量切片组织成批次|在两个潜变量之间插值|按系数缩放潜变量数值|计算两个潜变量的差|对潜变量执行指定运算|将潜变量运算接入 CFG 相关过程|创建潜空间锐化运算|创建潜空间色调映射运算|组织多个潜变量批次|连接两个潜变量批次|从潜变量批次取样|重组潜变量批次大小|重复潜变量批次|裁剪潜变量空间区域|翻转潜变量|旋转潜变量',
'B07': '显式选择采样算法和时间表进行采样|将噪声引导器算法时间表拆开采样|用单组条件构建引导器|用正负条件构建 CFG 引导器|向潜变量添加指定噪声|提供不加初始噪声的策略|按种子创建噪声策略|按名称选择采样算法|由模型与步数创建基础噪声时间表',
'B08': '使用 Align Your Steps 时间表|使用 Beta 分布时间表|使用指数时间表|使用 GITS 时间表|使用 Karras 时间表|使用 Laplace 时间表|使用 Optimal Steps 时间表|使用多项式指数时间表|使用 SD Turbo 时间表|使用 VP 时间表|在时间表中补充中间噪声级别|反转噪声级别序列|手工定义噪声时间表|将采样进度换算为 sigma|调整时间表首个噪声级别|按步数拆分时间表|按去噪比例拆分时间表',
'B09': '选择 Euler CFG++ 算法|选择自适应 DPM 算法|选择 DPM++ 2M SDE 算法|选择 DPM++ 2S Ancestral 算法|选择 DPM++ 3M SDE 算法|选择 DPM++ SDE 算法|选择 ER SDE 算法|选择 Euler Ancestral 算法|选择 Euler Ancestral CFG++ 算法|选择 LCM 算法|选择带潜空间放大的 LCM 算法|选择 LMS 算法|选择 SA Solver 算法|选择 SEEDS2 算法',
'B10': '对 CFG 引导进行归一化处理|使用 CFG Zero Star 引导修正|调整 LTX 音视频模态引导|调整 LTX 时空引导|使用 NAG 引导补丁|对 DiT 应用跳层引导|用简化接口设置 DiT 跳层引导|对 SD3 应用跳层引导|设置 TCFG 引导|调整引导中的频率分量|应用负向条件投影处理|构建 PerpNeg 引导器|应用 Mahiro 引导补丁|应用自注意力引导|应用自适应投影引导|覆盖模型 CFG 行为|构建双 CFG 引导器|构建双模型引导器|构建 LTX 双 CFG 引导器|沿视频进程设置线性 CFG 变化|沿视频进程设置三角形 CFG 变化',
'B11': '定义可复用的条件时间区间|按权重平均两组条件|合并多组条件条目|连接条件表示|缩放条件强度|调整区域条件强度|按比例指定视频条件作用区域|按比例指定图像条件作用区域|按像素指定条件作用区域|用遮罩限制条件作用区域|将条件表示置零做对照|限定条件作用的采样阶段',
'B12': '仅给生成模型加载 LoRA|用旁路方式给模型与编码器加载 LoRA|仅给生成模型旁路加载 LoRA|给模型与编码器加载匹配 LoRA|读取可复用的 LoRA 对象',
'B13': '编码 ControlNet 专用文本条件|控制 ControlNet 的强度与起止阶段|把结构控制信号加入条件|应用 AliMama 局部重绘控制|应用 SD3 专用 ControlNet|选择 Union ControlNet 的控制类型|加载 ControlNet 权重|加载差分 ControlNet 权重',
'B14': '用视觉特征给条件添加风格参考|将参考图片编码为视觉特征|把参考潜变量加入条件|构建 unCLIP 图像条件|为指定文本区域添加 GLIGEN 条件|构建 PhotoMaker 身份条件|加载视觉编码器|加载 GLIGEN 模型|加载 PhotoMaker 模型|加载风格模型|加载 unCLIP 模型组件',
'C01': '把帧序列和可选音轨封装成视频|从视频取出图像帧音轨和帧率|读取视频文件|保存已构建的视频|将图像帧编码成 WebM 文件',
'C02': '截短视频潜变量时间轴|替换视频潜变量的指定帧段|从视频按规则抽帧|按区间切分视频|随机裁剪视频时间片段|按指定位置裁剪视频时间片段',
'C03': '调整音频音量|调整低中高三个频段|首尾连接音频片段|创建静音音频|组合独立声道|读取音频文件|混合多段音频|试听中间音频|从录音控件采集音频|按高级选项保存音频|保存音频文件|将音频保存为 MP3|将音频保存为 Opus|拆出独立声道|按时间裁剪音频',
'C04': '用放大模型提高图片分辨率|加载插帧模型|加载潜空间放大模型|加载图像放大模型|在相邻帧之间生成中间帧',
'C05': '保持视频文本配对地打乱样本|读取视频数据集|读取视频与文本配对数据集|打乱视频数据集顺序',
'D01': '把图像视频音频参考组织为 H3 条件和初始潜变量|解码 H3 工作流分离出的音频潜变量|分块解码音频潜变量',
'D02': '用首帧或首末帧约束 H3 视频生成|为 H3 创建音视频联合初始潜变量',
'D03': '把参考画面放到 H3 指定时间位置',
'D04': '调整 H3 视频与音频的噪声时间映射',
'F01': '创建明确的三维相机参数|载入三维文件并取得视图图像与相机信息|用高级视图状态载入三维文件|预览三维文件|用高级相机与显示设置预览三维文件|预览点云|按高级设置保存三维文件|将三维结果保存为 GLB|保存点云文件',
'F02': '把 DA3 几何估计转换成网格|把 MoGe 点图转换成网格|从 MoGe 几何信息提取视场角|渲染 DA3 几何结果作检查|渲染 MoGe 几何结果作检查|从图像估计 DA3 几何|从图像估计 MoGe 几何|对全景图估计 MoGe 几何|加载 DA3 模型|加载 MoGe 模型',
'F03': '把网格转换成可保存三维文件|减少网格面数|修补网格孔洞|读取网格统计信息|合并多个网格|给网格着色|重新组织网格拓扑|渲染网格检查几何|旋转网格|平滑网格法线|焊接相近顶点',
'F04': '把纹理应用到网格|烘焙环境遮蔽贴图|从网格烘焙法线贴图|从体素颜色烘焙纹理|提取网格纹理为图像|渲染 UV 图集检查展开|为网格展开 UV',
'F05': '预览 Gaussian Splat|保存 Gaussian Splat 文件|把 splat 转成三维文件对象|把 splat 转成网格|从三维文件读取 splat|统计 splat 数量|合并多个 splat|渲染 splat 检查结果|对 splat 作空间变换',
'F06': '提取前景并移除背景|检测目标边界框|用 SAM3 检测或分割目标|加载背景移除模型',
'F07': '在视频帧中持续跟踪目标|预览跟踪结果与轨迹|把跟踪结果转换为遮罩',
'F08': '加载 SAM3D 人体姿态模型|渲染人体姿态预测结果|从人物图像或视频帧预测三维姿态',
'F09': '减少连续人体姿态的帧间抖动',
'F10': '把人体姿态导出为动画 GLB 或 BVH 动捕文件',
'F11': '提取面部关键点|按面部关键点生成遮罩|将面部表情信息应用到人体姿态|可视化面部网格与关键点|加载面部关键点模型',
'F12': '将姿态关键点绘制为图像|由姿态关键点获得脸部边界框|从图像提取人体姿态关键点',
'G01': '调整 CLIP 注意力乘数|调整生成模型交叉注意力|调整生成模型自注意力|调整生成模型时间注意力|手工设置上下文窗口|设置 LTX 专用上下文窗口|选择模型注意力后端|调整模型噪声尺度|设置 AuraFlow 采样映射|设置连续 EDM 采样映射|设置连续 V 参数化采样映射|设置离散采样映射|对 CFG 进行重新归一化|重缩放 CFG 引导|调整旋转位置编码尺度|设置 Wan 上下文窗口|设置 Chroma Radiance 专用选项|设置 Flux 采样映射|平滑 HiDream O1 接缝|设置 LTX 采样映射|设置 Stable Cascade 采样映射|设置 SD3 采样映射|调整 epsilon 缩放|应用 FreeU 特征调整|应用第二版 FreeU 特征调整|分块执行部分模型计算|在模型内部添加下采样补丁|应用扰动注意力引导|合并 token 以探索计算开销变化|调整时间维度预测分数',
'G02': '把 Hook 绑定到文本编码器|合并两组 Hook|合并四组 Hook|合并八组 Hook|合并成对正负条件|合并成对条件并设置默认项|为成对条件设置属性|设置成对条件属性并合并|合并条件并设置默认项|设置条件属性|设置条件属性并合并|从 LoRA 创建模型与编码器 Hook|从 LoRA 创建模型 Hook|从模型差异创建模型与编码器 Hook|从模型差异创建模型 Hook|创建单个 Hook 关键帧|从浮点列表创建 Hook 关键帧|创建插值 Hook 关键帧|把关键帧时间安排绑定到 Hook',
'G03': '保存 LoRA 差分结果|将两份 CLIP 权重相加|插值合并 CLIP 权重|计算 CLIP 权重差|保存 CLIP 权重|保存图像条件 checkpoint|将两份模型权重相加|分块合并模型权重|插值合并模型权重|计算模型权重差|保存模型权重|保存 checkpoint 组件|保存训练产生的 LoRA 对象|保存 VAE 权重|按 AuraFlow 层结构合并权重|按 Cosmos 14B 层结构合并权重|按 Cosmos 7B 层结构合并权重|按 Cosmos Predict2 14B 层结构合并权重|按 Cosmos Predict2 2B 层结构合并权重|按 Flux1 层结构合并权重|按 Krea2 层结构合并权重|按 LTX 层结构合并权重|按 Mochi 层结构合并权重|按 Qwen Image 层结构合并权重|按 SD1 层结构合并权重|按 SD2 层结构合并权重|按 SD3.5 Large 层结构合并权重|按 SD3 2B 层结构合并权重|按 SDXL 层结构合并权重|按 Wan2.1 层结构合并权重',
'G04': '用 EasyCache 探索计算复用|用 LazyCache 探索计算复用|选择模型计算精度|划分多 GPU 工作单元|指定文本编码器设备|指定生成模型设备|指定 VAE 设备|启用 Flux KV 缓存|对模型使用 torch.compile',
'G05': '回读编码后的训练数据|将图文样本制作为训练数据|观察训练损失曲线|按分辨率将训练样本分桶|保存编码后的训练数据|用已准备数据训练 LoRA',
'G06': '识别旧工作流的 Wan Block Swap 弃用占位并迁移',
'E01': '编码 SD3 文本条件|编码 SDXL Refiner 文本条件|编码 SDXL 文本与尺寸条件|创建 SD3 初始潜变量',
'E02': '编码 Flux 文本条件|选择 Flux Kontext 多参考潜变量方法|关闭条件中的 Flux guidance 配置|设置条件中的 Flux guidance 配置|预处理 Flux Kontext 参考图片尺寸|创建 Flux2 初始潜变量|建立 USO 风格参考|创建 Flux2 噪声时间表',
'E03': '编码 Qwen Image 编辑指令与参考图|编码 Qwen Image 多参考编辑条件|创建 Qwen Image 分层潜变量|应用 Qwen Image DiffSynth 控制模型',
'E04': '编码 HiDream 文本条件|为 HiDream O1 组织参考图|创建 HiDream O1 初始潜变量',
'E05': '编码 Boogu 图像编辑条件|编码 HunyuanDiT 文本条件|编码 Joy 图像编辑条件|编码 Lumina2 文本条件|编码 MageFlow 图像编辑条件|编码 PixArtAlpha 文本与尺寸条件|编码 ZImage Omni 多模态条件|创建 Chroma Radiance 初始潜变量|创建 HunyuanImage 初始潜变量|应用 ZImage Fun 控制模型',
'E06': '对重绘模型应用 Differential Diffusion|构建 Stable Cascade 超分条件|构建 PiD 专用条件|构建 InstructPixToPix 编辑条件|构建 Lotus 专用条件|构建 Stable Cascade Stage B 条件|构建 SD 4X 超分条件|创建 Stable Cascade 多阶段潜变量|用 Stage C VAE 编码图片',
'E07': '预测 LTX 生成时长相关信息|读取 IC-LoRA 控制参数|向 LTX 条件添加参考音频|给 LTX 添加指定位置的参考画面|设置 LTX 视频条件|移除 LTX 引导占用的潜变量帧|构建 LTX 图生视频输入|在已有 LTX 潜变量上加入图像条件|组合 LTX 音视频潜变量|创建 LTX 视频初始潜变量|解码 LTX 音频潜变量|编码 LTX 音频参考|创建 LTX 音频初始潜变量|放大 LTX 潜变量|拆分 LTX 音视频潜变量|加载 LTX 音视频文本编码器|加载 LTX 音频 VAE|创建 LTX 噪声时间表|预处理 LTX 输入图像',
'E08': '准备 Hunyuan 精修潜变量|准备 HunyuanVideo1.5 超分阶段输入|构建 Hunyuan 图生视频条件|构建 HunyuanVideo1.5 图生视频条件|编码 Hunyuan 视频图文条件|用模型放大 HunyuanVideo1.5 潜变量|创建 Hunyuan 视频初始潜变量|创建 HunyuanVideo1.5 初始潜变量',
'E09': '规范化视频潜变量起始部分|构建 Cosmos 图生视频潜变量|构建 Cosmos Predict2 图生视频潜变量|编码 Kandinsky5 文本条件|构建 Kandinsky5 图生视频条件|构建 SVD 图像条件|创建 Cosmos 视频初始潜变量|创建 Mochi 视频初始潜变量',
'E10': '构建自回归视频的图像输入|创建自回归视频初始潜变量|创建自回归视频采样算法',
'E11': '构建 Wan2.2 图生视频潜变量|为 Wan 设置首末帧条件|为 Wan 设置图生视频条件',
'E12': '构建 Wan 相机运动表示|把相机运动用于 Wan 图生视频|生成运动轨迹|连接多组 WanMove 轨迹|从坐标建立 WanMove 轨迹|将 WanMove 轨迹加入视频条件|可视化 WanMove 运动轨迹|将运动轨迹加入 Wan 视频条件',
'E13': '构建 Wan2.2 Fun 控制条件|构建 Wan Fun 控制条件|构建 Wan Fun 视频修补条件|构建 Wan Phantom 主体参考条件|构建 Wan VACE 编辑条件|应用 Wan Uni3C 控制模型',
'E14': '给 Wan Animate2 应用缓存|构建 Wan Animate2 动作驱动条件|构建 Wan Animate 动作驱动条件|构建 SCAIL2 人体颜色遮罩|构建 Wan SCAIL 动作条件',
'E15': '填充 WanDancer 关键帧|填充 WanDancer 关键帧列表|提取音频编码特征|提取 WanDancer 专用音频特征|构建 WanDancer 音频驱动视频条件|构建 Wan HuMo 图生视频条件|构建 Wan InfiniteTalk 说话视频条件|构建 Wan 音频驱动图生视频条件|续接 Wan 音频驱动视频|加载音频特征编码器',
'E16': '预处理 VOID 四类区域遮罩|构建 VOID 视频修补条件|使用光流扭曲潜变量噪声|创建 VOID 光流噪声来源|加载光流模型|创建 VOID 专用采样算法',
'E17': '将体素结果转换为网格|用基础转换器把体素转为网格|构建 Hunyuan3D 单视图条件|构建 Hunyuan3D 多视图条件|创建 Hunyuan3D 初始潜变量|解码 Hunyuan3D 潜变量为体素',
'E18': '构建 Bernini 三维条件|构建 Pixal3D 三维条件|准备 Trellis2 放大阶段|构建 Trellis2 图像条件|准备 Trellis2 形状阶段|准备 Trellis2 纹理阶段|创建 Trellis2 结构初始潜变量|解码 Trellis 形状|解码 Trellis2 结构|解码 Trellis 纹理体素',
'E19': '构建 TripoSplat 图像条件|预处理 TripoSplat 参考图片|将 TripoSplat 潜变量解码成 splat|预览 TripoSplat 采样过程',
'E20': '构建 SV3D 多视角条件|构建 Stable Zero123 视角条件|构建 Stable Zero123 批量视角条件',
'E21': '加入参考音色条件|编码 ACE-Step 音乐文本条件|编码 ACE-Step1.5 音乐文本条件|编码 MiniMaxMusic3 音乐条件|构建 Stable Audio 条件|创建通用音频模型所需初始潜变量|将音频编码为潜变量|创建 ACE-Step 初始潜变量|创建 ACE-Step1.5 初始潜变量|创建 MiniMaxMusic3 初始潜变量',
'E22': '对 SeedVR2 输出作后处理|预处理 SeedVR2 输入|构建 SeedVR2 修复条件|合并 SeedVR2 时间块|拆分 SeedVR2 时间块|将 SUPIR 修复配置应用到模型',
'E23': '创建 Ideogram4 噪声时间表|用文本生成模型整理 LTX2 视频提示词|用兼容语言模型生成或改写文本',
'E24': '加载 Hypernetwork 补丁|读取专用模型补丁权重|应用 Anima LLLite 控制补丁',
}

GOALS = {
'A01':'检查工作流输入、中间结果和最终输出','A02':'让多个节点共享参数或按输入自动计算参数','A03':'整理提示词、批量标签和结构化文本','A04':'按条件选择工作流路径','A05':'为后续合成或模型输入准备合适的构图和尺寸','A06':'修整画面或准备图像处理对照','A07':'指定局部重绘、抠图或合成的作用区域','A08':'制作透明素材或把主体放入新背景','A09':'批量处理图片、制作对照图或分块处理大图','A10':'用位置明确的区域组织画面元素','A11':'创建输入素材或按交付格式输出','A12':'准备批量图文处理或训练样本','A13':'现有图像节点无法表达所需像素运算',
'B01':'搭建模型加载与文本条件编码流程','B02':'在可见图像与模型潜空间之间转换','B03':'建立基础文生图闭环','B04':'实现分段采样、续采样或控制去噪范围','B05':'只重绘画面的局部区域','B06':'复用、组合或修改采样中间状态','B07':'独立控制采样过程的噪声、引导、算法和时间表','B08':'在相同模型下对比噪声步长安排','B09':'在相同噪声与条件下比较采样方法','B10':'在兼容模型上探索条件引导的行为','B11':'组合多组提示或限定它们的作用区域和阶段','B12':'让兼容基础模型使用附加风格或任务适配权重','B13':'用边缘、姿态、深度或其他控制信号约束生成','B14':'用图像特征、身份或区域布局补充文本条件',
'C01':'在视频文件与帧序列之间转换','C02':'截取或替换视频时间片段','C03':'处理对白、背景音乐或生成音轨','C04':'提高图像分辨率或视频时间采样密度','C05':'组织视频训练或批量处理样本','D01':'搭建 H3 多模态参考视频工作流','D02':'从参考画面开始生成 H3 视频','D03':'要求 H3 在特定时刻出现参考画面','D04':'对比 H3 音视频采样配置',
'F01':'检查或交付三维资产','F02':'从图像建立可检查的三维几何','F03':'清理、合并或简化三维几何','F04':'为三维资产准备纹理与材质输入','F05':'检查、变换或交付 Gaussian Splat','F06':'自动定位人物或其他主体','F07':'让同一目标在连续视频帧中保持对应关系','F08':'从人物素材获得可渲染的三维姿态','F09':'改善逐帧姿态预测产生的时间抖动','F10':'将已获得的动作交给三维软件继续制作','F11':'处理人体动作中的脸部区域与表情','F12':'准备二维姿态图或脸部区域',
'G01':'在匹配架构上对比模型运行方式或注意力配置','G02':'让适配权重和条件在指定阶段生效','G03':'研究同架构权重组合并保存可回读结果','G04':'在固定任务下比较速度、显存与输出误差','G05':'建立最小 LoRA 训练与回读闭环','G06':'维护包含弃用节点的旧工作流',
'E01':'使用 SDXL 或 SD3 家族模板','E02':'使用 Flux 家族生成或参考编辑模板','E03':'使用 Qwen Image 编辑或分层模板','E04':'使用 HiDream 家族模板','E05':'使用本节点名称所对应的图像模型模板','E06':'使用多阶段、超分或专项图像模型模板','E07':'使用 LTX 视频或音视频联合模板','E08':'使用 Hunyuan 视频或超分模板','E09':'使用本节点对应的 Cosmos、Kandinsky、Mochi 或 SVD 模板','E10':'使用自回归视频模板','E11':'使用 Wan 图生视频模板','E12':'控制 Wan 视频中的运动路径或相机','E13':'使用 Wan 控制、修补或主体参考模板','E14':'使用 Wan 人体动作驱动模板','E15':'使用 Wan 音频驱动或说话视频模板','E16':'使用 VOID 视频修补模板','E17':'使用 Hunyuan3D 生成模板','E18':'使用对应的 Trellis、Bernini 或 Pixal3D 模板','E19':'使用 TripoSplat 生成模板','E20':'从参考主体生成新视角','E21':'使用本节点对应的音频生成模型模板','E22':'使用 SeedVR2 或 SUPIR 修复模板','E23':'为图像或视频任务准备语言生成与专用采样组件','E24':'为兼容基础模型添加专用控制能力',
}

# Known source nodes for general interfaces. These are alternative examples,
# not a requirement to run every producer in the list.
SOURCES={
'IMAGE':['LoadImage'], 'MASK':['LoadImageMask','SolidMask'], 'AUDIO':['LoadAudio'], 'VIDEO':['LoadVideo','CreateVideo'],
'MODEL':['UNETLoader','CheckpointLoaderSimple'], 'CLIP':['CLIPLoader','DualCLIPLoader'], 'VAE':['VAELoader'],
'CONDITIONING':['CLIPTextEncode'], 'LATENT':['VAEEncode','EmptyLatentImage'],
'MESH':['DA3GeometryToMesh','MoGePointMapToMesh'], 'SPLAT':['File3DToSplat','VAEDecodeTripoSplat'],
'FILE_3D':['Load3DAdvanced'], 'FILE_3D_GLB':['MeshToFile3D'], 'FILE_3D_SPLAT_ANY':['SplatToFile3D'],
'LOAD3D_CAMERA':['CreateCameraInfo','Load3DAdvanced'], 'LOAD3D_MODEL_INFO':['Load3DAdvanced'],
'CLIP_VISION':['CLIPVisionLoader'], 'CLIP_VISION_OUTPUT':['CLIPVisionEncode'], 'CONTROL_NET':['ControlNetLoader'],
'MHR_POSE_DATA':['SAM3DBody_Predict','SAM3DBody_Smooth'], 'SAM3D_BODY_MODEL':['SAM3DBody_Loader'],
'SAM3_TRACK_DATA':['SAM3_VideoTrack'], 'BOUNDING_BOX':['PrimitiveBoundingBox','RTDETR_detect'],
'FACE_LANDMARKS':['MediaPipeFaceLandmarker'], 'POSE_KEYPOINT':['SDPoseKeypointExtractor'],
'DA3_GEOMETRY':['DA3Inference'], 'MOGE_GEOMETRY':['MoGeInference'], 'DA3_MODEL':['LoadDA3Model'], 'MOGE_MODEL':['LoadMoGeModel'],
'BACKGROUND_REMOVAL':['LoadBackgroundRemovalModel'], 'FACE_DETECTION_MODEL':['LoadMediaPipeFaceLandmarker'],
'UPSCALE_MODEL':['UpscaleModelLoader'], 'INTERP_MODEL':['FrameInterpolationModelLoader'], 'LATENT_UPSCALE_MODEL':['LatentUpscaleModelLoader'],
'MODEL_PATCH':['ModelPatchLoader'], 'PHOTOMAKER':['PhotoMakerLoader'], 'STYLE_MODEL':['StyleModelLoader'], 'GLIGEN':['GLIGENLoader'],
'AUDIO_ENCODER':['AudioEncoderLoader'], 'AUDIO_ENCODER_OUTPUT':['AudioEncoderEncode'],
'OPTICAL_FLOW':['OpticalFlowLoader'], 'GUIDER':['BasicGuider','CFGGuider'], 'SAMPLER':['KSamplerSelect'], 'NOISE':['RandomNoise','DisableNoise'],
'SIGMAS':['BasicScheduler'], 'LATENT_OPERATION':['LatentOperationSharpen','LatentOperationTonemapReinhard'],
'HOOKS':['CreateHookLora','CreateHookLoraModelOnly'], 'HOOK_KEYFRAMES':['CreateHookKeyframe'], 'TIMESTEPS_RANGE':['ConditioningTimestepsRange'],
'LORA_MODEL':['TrainLoraNode'], 'LOSS_MAP':['TrainLoraNode'], 'LAYERS':['AddLayer','LayersFromBoundingBoxes'],
'WAN_CAMERA_EMBEDDING':['WanCameraEmbedding'], 'TRACKS':['GenerateTracks','WanMoveTracksFromCoords'],
'IC_LORA_PARAMETERS':['GetICLoRAParameters'], 'VOXEL':['VAEDecodeHunyuan3D','VaeDecodeStructureTrellis2'], 'SHAPE_SUBDIVIDES':['VaeDecodeShapeTrellis'],
'ARRAY':['CreateBoundingBoxes'], 'DICT':['BuildJsonPromptIdeogram'], 'CURVE':['CurveEditor'], 'HISTOGRAM':['ImageHistogram'],
}
WIDGETS={'LOAD_3D':'节点的三维视图控件','AUDIO_RECORD':'节点的录音控件','WEBCAM':'节点的摄像头控件','COMPOSITOR':'节点的图层编辑器','BOUNDING_BOXES':'节点的边界框编辑器','COLORS':'节点的调色板控件','IMAGECOMPARE':'节点的图像对照控件','COLOR':'颜色控件（按当前界面填写）'}
SCALARS={'STRING','INT','FLOAT','BOOLEAN','COMBO','FLOAT,INT','INT,FLOAT,STRING,BOOLEAN'}
SENSITIVE={'MODEL','CLIP','VAE','LATENT','CONDITIONING','CLIP_VISION','CLIP_VISION_OUTPUT','CONTROL_NET','MODEL_PATCH','AUDIO_ENCODER','AUDIO_ENCODER_OUTPUT','VOXEL','SHAPE_SUBDIVIDES','LORA_MODEL','LATENT_UPSCALE_MODEL','HOOKS','HOOK_KEYFRAMES','GUIDER','IC_LORA_PARAMETERS'}
# Per-node overrides take precedence over generic examples. [] means no
# safe fixed-index producer can be asserted; document the gap instead.
OVERRIDES={
('BuildPoseFile','pose_data'):['SAM3DBody_Smooth','SAM3DBody_Predict'],
('SAM3DBody_Smooth','mhr_pose_data'):['SAM3DBody_Predict'],
('TextGenerate','clip'):['CLIPLoader'],('TextGenerateLTX2Prompt','clip'):['CLIPLoader'],
('TextGenerate','video'):['GetVideoComponents'],
('KSampler','latent_image'):['EmptyLatentImage','VAEEncode'],('KSamplerAdvanced','latent_image'):['VAEEncode','EmptyLatentImage'],
('VAEDecode','samples'):['KSampler','SamplerCustomAdvanced'],('VAEDecodeTiled','samples'):['KSampler','SamplerCustomAdvanced'],
('TrainLoraNode','latents'):['LoadTrainingDataset','MakeTrainingDataset'],('TrainLoraNode','positive'):['LoadTrainingDataset','MakeTrainingDataset'],
('SaveTrainingDataset','latents'):['MakeTrainingDataset'],('SaveTrainingDataset','conditioning'):['MakeTrainingDataset'],
('ResolutionBucket','latents'):['MakeTrainingDataset','LoadTrainingDataset'],
('LTXVSeparateAVLatent','av_latent'):['SamplerCustomAdvanced','LTXVConcatAVLatent'],
('File3DToSplat','model_3d'):['SplatToFile3D'],
}

DYNAMIC={
('MiniMaxH3ReferenceToVideo','ref_images'):['LoadImage'],('MiniMaxH3ReferenceToVideo','ref_videos'):['GetVideoComponents'],
('MiniMaxH3ReferenceToVideo','ref_video_audios'):['GetVideoComponents'],('MiniMaxH3ReferenceToVideo','ref_audios'):['LoadAudio'],
('GLSLShader','images'):['LoadImage'],('GLSLShader','curves'):['CurveEditor'],
('GLSLShader','floats'):['PrimitiveFloat'],('GLSLShader','ints'):['PrimitiveInt'],('GLSLShader','bools'):['PrimitiveBoolean'],
('ComfyMathExpression','values'):['PrimitiveInt','PrimitiveFloat'],
('BatchImagesNode','images'):['LoadImage'],('BatchMasksNode','masks'):['LoadImageMask'],
('MergeMeshes','meshes'):['DA3GeometryToMesh','MoGePointMapToMesh'],('MergeSplat','splats'):['File3DToSplat'],
('BerniniConditioning','reference_images'):['LoadImage'],('TextEncodeBooguEdit','images'):['LoadImage'],
('HiDreamO1ReferenceImages','images'):['LoadImage'],('TextEncodeJoyImageEdit','images'):['LoadImage'],('TextEncodeMageFlowEdit','images'):['LoadImage'],
('BatchLatentsNode','latents'):['VAEEncode'],('StringFormat','values'):['PrimitiveString'],('CreateList','inputs'):['PrimitiveString','PrimitiveInt'],
('ComfyAndNode','values'):['PrimitiveBoolean'],('ComfyOrNode','values'):['PrimitiveBoolean'],
}

SPECIAL_SCENARIOS={
'KSampler':['从空潜变量开始，根据提示词生成图片。','把输入图编码成潜变量后进行图生图，通过 denoise 控制允许改变的幅度。'],
'KSamplerAdvanced':['将采样拆成多个阶段，让不同条件或模型处理不同步段。','续接已有中间潜变量，显式控制是否加噪及起止步数。'],
'VAEEncode':['把参考图片转成匹配模型的潜变量，作为图生图或潜空间处理的输入。'],
'VAEDecode':['采样器输出无法直接作为图片查看时，用同家族 VAE 解码后接预览或保存。'],
'CLIPLoader':['工作流采用分离权重时，单独加载生成模型所需的文本编码器。','为 TextGenerate 准备模型时，选择当前实现支持的生成式语言模型，不能随意选普通 CLIP 权重。'],
'CheckpointLoaderSimple':['用一个兼容 checkpoint 建立基础生成流程，并将模型、CLIP、VAE 分别交给采样、编码和解码节点。'],
'ImageCrop':['从人物全身参考图提取脸部或主体区域，供后续编辑或对照；坐标和裁剪尺寸由参数控制。'],
'ImageScale':['把素材调整到后续节点所需的宽高，或在同一尺寸下比较多张参考图片。'],
'AdjustBrightness':['合成前修正主体与背景的明暗差异，或制作亮度参数的单变量对照。'],
'SAM3DBody_Predict':['把人物图片或视频帧转换为三维动作数据，供平滑、姿态渲染或动画导出。','多人视频中结合跟踪信息区分人物；单人基础实验可从简单清晰素材开始。'],
'MiniMaxH3ReferenceToVideo':['把角色参考图、动作参考视频或参考音频组织成 H3 条件，供后续采样生成视频。','多参考素材需要按编号在提示词中引用时，集中维护参考输入与标签对应关系。'],
'MiniMaxH3ImageToVideo':['让 H3 从给定首帧开始生成动作；有明确结束画面时再提供末帧。'],
'MiniMaxH3AddGuide':['视频中间某个时刻需要出现指定画面或音频参考时，在已有 H3 条件上加入时间锚点。'],

'TextGenerate':['把简短创作意图扩写为提示词，或将已有文本改写、总结后交给文本处理节点。','模型支持相应模态时，依据图片、视频帧或音频生成描述；它输出文本，不直接输出生成图片。'],
'BuildPoseFile':['将人物动作预测结果导出为带动画的 GLB，在三维查看器中检查并交付。','需要把单人骨架动作交给动画软件继续制作时导出 BVH；材质与蒙皮交付要求另行核对。'],
'SAM3DBody_Smooth':['连续帧的人体姿态出现细碎抖动时，在渲染或动画导出前做时间平滑。','快速转身或抬手需要保留时，对照平滑强度和窗口，避免把真实运动一起抹平。'],
'CLIPTextEncode':['将正向或负向提示词编码为采样器/引导器需要的 CONDITIONING；正负通常使用两个节点实例。'],
'LoadImage':['将本地参考图接入裁剪、合成、图生图或图生视频流程；透明图的 MASK 含义另按实验核对。'],
'PreviewImage':['在裁剪、遮罩合成或 VAE 解码后检查画面，快速判断是哪一步开始出现偏差。'],
'SaveImage':['将最终图片落盘交付，或保存参数 A/B 对照的两份输出以做像素比较。'],
'wanBlockSwap':['加载旧工作流时识别兼容占位；先核对当前版本的弃用行为，不把它当作仍有效的显存优化。'],
}

def build_context(schemas,groups):
    by={n['class_name']:n for n in schemas}; members={k:g for g in groups for k in g['nodes']}
    ops={}
    for g in groups:
        seq=OPERATIONS[g['id']].split('|')
        assert len(seq)==len(g['nodes']),(g['id'],len(seq),len(g['nodes']))
        ops.update(zip(g['nodes'],seq))
    result={}
    for n in schemas:
        k=n['class_name'];g=members[k];deps=[]
        for i in n['inputs']:
            if i['required']=='hidden':continue
            typ=i['type'];name=i['name'];key=(k,name)
            row=dict(input=name,type=typ,requirement=i['required'],sources=[],note='',kind='connection')
            if typ in SCALARS:
                # Widgets can often become inputs, but are not forced upstream dependencies.
                row.update(kind='parameter',note='在本节点填写；若当前界面支持转为输入，也可连接同类型参数节点。不强制依赖上游。')
            elif typ in WIDGETS:
                row.update(kind='widget',note=WIDGETS[typ]+'提供状态；不是缺失的模型加载器。')
            elif typ.startswith('COMFY_') or typ=='*':
                row.update(kind='dynamic',note='动态/通配接口：先在当前界面展开实际子端口，再核对类型、数量及列表语义；候选不代表顶层可直接连线。')
                if typ=='COMFY_DYNAMICCOMBO_V3':row['note']='本节点选择模式并展开子参数；子输入依赖随所选模式变化，固定索引未展开全部分支。'
                elif typ=='*':row['note']='取决于要观察的对象；可先用 PrimitiveString 做文本观察，非唯一前置。'
                for source in DYNAMIC.get(key,(['PrimitiveString'] if typ=='*' else [])):
                    output=by[source]['outputs'][0]['name']
                    if key==('MiniMaxH3ReferenceToVideo','ref_videos'):output='images'
                    elif key==('MiniMaxH3ReferenceToVideo','ref_video_audios'):output='audio'
                    row['sources'].append(dict(node=source,output=output,basis='dynamic_candidate'))
                if key==('MiniMaxH3ReferenceToVideo','ref_videos'):
                    row['note']+=' 已核对项目留存 H3 源码：ref_video_* 子端口接 IMAGE 帧批次，按 24 FPS 准备，不直接接 VIDEO。'
                elif key==('MiniMaxH3ReferenceToVideo','ref_video_audios'):
                    row['note']+=' 音轨必须与同编号参考视频对应，不能任意拿另一段声音代替。'
            else:
                accepted=set(typ.split(','));names=OVERRIDES.get(key)
                if names is None:
                    names=[]
                    for t in typ.split(','):
                        names+=SOURCES.get(t,[])
                if typ=='CONDITIONING' and key not in OVERRIDES:
                    if k.startswith('MiniMaxH3'):
                        names=['MiniMaxH3ReferenceToVideo','MiniMaxH3ImageToVideo']
                    elif k.startswith(('Flux','USO')):names=['CLIPTextEncodeFlux']
                    elif k.startswith('HiDream'):names=['CLIPTextEncodeHiDream']
                    elif k.startswith('Kandinsky'):names=['CLIPTextEncodeKandinsky5']
                    elif k.startswith('Trellis2'):names=['Trellis2Conditioning']
                    elif k.startswith('ReferenceTimbre'):names=['TextEncodeAceStepAudio']
                    elif k.startswith('LTXV') and k!='LTXVConditioning':names=['LTXVConditioning']
                    elif k.startswith('Hunyuan') and '15' not in k: names=['TextEncodeHunyuanVideo_ImageToVideo']
                if typ=='LATENT' and key not in OVERRIDES:
                    if g['id'].startswith(('D','E')) or any(x in k for x in ('LTX','Hunyuan','Wan','Trellis','TripoSplat')):
                        names=['SamplerCustomAdvanced']
                        row['note']='来自同一模型模板中对应阶段的采样输出候选；不是任意基础图像 latent。'
                    if k=='MiniMaxH3AddGuide':names=['MiniMaxH3ReferenceToVideo','MiniMaxH3ImageToVideo']
                    elif k in ('VAEDecodeAudio','VAEDecodeAudioTiled','LTXVAudioVAEDecode'):names=['LTXVSeparateAVLatent']
                    elif k=='LTXVConcatAVLatent':names=['EmptyLTXVLatentVideo'] if name=='video_latent' else ['LTXVEmptyLatentAudio','LTXVAudioVAEEncode']
                    elif k=='LTXVAddGuide':names=['EmptyLTXVLatentVideo','LTXVImgToVideo']
                    elif k=='LTXVImgToVideoInplace':names=['EmptyLTXVLatentVideo']
                    elif k=='SeedVR2Conditioning':names=['VAEEncode']
                    elif k=='SeedVR2TemporalChunk':names=['VAEEncode']
                    elif k=='VOIDWarpedNoiseSource':names=['VOIDWarpedNoise']
                    elif k=='LTXVScheduler' or k=='ModelSamplingLTXV':names=['EmptyLTXVLatentVideo','LTXVConcatAVLatent']
                    elif k=='ReferenceTimbreAudio':names=['VAEEncodeAudio']
                if k=='CreateHookKeyframe' and name=='prev_hook_kf':
                    names=['CreateHookKeyframesInterpolated']
                    row['note']='可不接；连接时来自此前独立创建的关键帧对象，也可使用另一个 CreateHookKeyframe 实例的输出，不能接回本实例。'
                if k=='CurveEditor' and name=='curve':
                    row['note']='可选已有曲线；可由另一个 CurveEditor 实例提供，也可在本节点直接编辑，不要求连接回自身。'
                if k=='LoraSave':names=['ModelMergeSubtract'] if typ=='MODEL' else ['CLIPMergeSubtract'] if typ=='CLIP' else names
                for source in dict.fromkeys(names):
                    if source==k:continue
                    assert source in by,source
                    outputs=[o for o in by[source]['outputs'] if set(o['type'].split(','))&accepted]
                    output=next((o for o in outputs if o['name']==name), outputs[0] if outputs else None)
                    if source=='LTXVSeparateAVLatent' and name=='samples':
                        output=next(o for o in outputs if o['name']=='audio_latent')
                    if output:row['sources'].append(dict(node=source,output=output['name'],basis='port_candidate' if accepted&SENSITIVE else 'interface_example'))
                if not row['note']:
                    row['note']='接口来源示例，可选其一或使用等价上游；不是要求全部连接。'
                if accepted&SENSITIVE:
                    row['note']+=' 必须核对模型家族、权重、张量布局及阶段；端口同名不保证兼容。'
                if not row['sources'] and k!='CurveEditor':
                    row['note']+=' 固定索引尚未确定本页可直接采用的上游，标记待核对；不要自连接或凭名称强行补齐。'
                if 'KIMODO_POSE_DATA' in accepted:row['note']+=' 表中示例仅覆盖 MHR；固定索引缺 Kimodo 生产者。'
            if k=='TextGenerate' and name=='clip':row['note']='CLIPLoader 必须加载当前 ComfyUI 支持、具备文本生成能力的语言模型；普通 CLIP 编码器不能因此替代。模型权重是外部依赖。'
            if k=='TextGenerateLTX2Prompt' and name=='clip':row['note']='加载该节点当前模板要求、具有生成能力的语言模型；不能用普通 CLIP 编码器替代。'
            if k=='BuildPoseFile' and name=='sam3d_body_model':row['note']='接口标 optional，但 MHR 的 BVH/网格/骨骼等分支可能需要模型；具体条件和无模型负例见本页用例。'
            if k in ('PreviewPointCloud','SavePointCloud') and name=='model_3d':
                row['note']='需要兼容的外部点云文件；本索引未给出独立点云加载生产者。先核对当前版本文件上传/导入入口，不能让预览和保存彼此循环充当初始来源。'
            deps.append(row)
        # Learning prerequisites are selected producer pages, not every member of a prerequisite group.
        learning=list(dict.fromkeys(x['node'] for d in deps if d['kind']=='connection' for x in d['sources']))
        result[k]=dict(class_name=k,operation=ops[k],scenarios=SPECIAL_SCENARIOS.get(k,[GOALS[g['id']]+'时，用于'+ops[k]+'。']),dependencies=deps,learning_nodes=learning,status='design_not_run',basis='fixed_index_and_authored_scenarios')
    return result
