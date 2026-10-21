# 逐节点实验目录

每个节点都有独立实验卡；先按[实验组依赖](../labs/README.md)准备上游，再执行卡内A/B对照。**所有用例尚未运行；覆盖设计不等于验证通过。**

[测量规则](../guides/observable-results.md) · [结果模板](../templates/node-experiment-record.md)

## A01 建立观察与保存出口

| 节点 | 用例数 |
|---|---|
| [ImageCompare](A01/ImageCompare.md) | 2 |
| [GetImageSize](A01/GetImageSize.md) | 2 |
| [LoadImage](A01/LoadImage.md) | 2 |
| [LoadImageOutput](A01/LoadImageOutput.md) | 2 |
| [PreviewImage](A01/PreviewImage.md) | 2 |
| [SaveImage](A01/SaveImage.md) | 2 |
| [PreviewAny](A01/PreviewAny.md) | 2 |

## A02 把参数变成数据

| 节点 | 用例数 |
|---|---|
| [ColorToRGBInt](A02/ColorToRGBInt.md) | 1 |
| [ComfyNumberConvert](A02/ComfyNumberConvert.md) | 1 |
| [CreateList](A02/CreateList.md) | 2 |
| [CurveEditor](A02/CurveEditor.md) | 1 |
| [CustomCombo](A02/CustomCombo.md) | 2 |
| [ComfyMathExpression](A02/ComfyMathExpression.md) | 2 |
| [ResolutionSelector](A02/ResolutionSelector.md) | 2 |
| [SeedNode](A02/SeedNode.md) | 2 |
| [PrimitiveBoolean](A02/PrimitiveBoolean.md) | 2 |
| [PrimitiveFloat](A02/PrimitiveFloat.md) | 2 |
| [PrimitiveInt](A02/PrimitiveInt.md) | 2 |
| [PrimitiveString](A02/PrimitiveString.md) | 2 |
| [PrimitiveStringMultiline](A02/PrimitiveStringMultiline.md) | 2 |

## A03 确定性文本处理

| 节点 | 用例数 |
|---|---|
| [AddTextPrefix](A03/AddTextPrefix.md) | 1 |
| [AddTextSuffix](A03/AddTextSuffix.md) | 1 |
| [BuildJsonPromptIdeogram](A03/BuildJsonPromptIdeogram.md) | 1 |
| [StringCompare](A03/StringCompare.md) | 1 |
| [StringConcatenate](A03/StringConcatenate.md) | 1 |
| [StringContains](A03/StringContains.md) | 2 |
| [ConvertArrayToString](A03/ConvertArrayToString.md) | 1 |
| [ConvertDictionaryToString](A03/ConvertDictionaryToString.md) | 1 |
| [CaseConverter](A03/CaseConverter.md) | 1 |
| [TextToLowercase](A03/TextToLowercase.md) | 1 |
| [TextToUppercase](A03/TextToUppercase.md) | 1 |
| [TextOverlay](A03/TextOverlay.md) | 2 |
| [RegexExtract](A03/RegexExtract.md) | 2 |
| [JsonExtractString](A03/JsonExtractString.md) | 2 |
| [StringFormat](A03/StringFormat.md) | 2 |
| [RegexMatch](A03/RegexMatch.md) | 2 |
| [MergeTextLists](A03/MergeTextLists.md) | 2 |
| [StringReplace](A03/StringReplace.md) | 1 |
| [ReplaceText](A03/ReplaceText.md) | 1 |
| [RegexReplace](A03/RegexReplace.md) | 2 |
| [SaveText](A03/SaveText.md) | 2 |
| [StripWhitespace](A03/StripWhitespace.md) | 2 |
| [StringSubstring](A03/StringSubstring.md) | 2 |
| [StringLength](A03/StringLength.md) | 1 |
| [StringTrim](A03/StringTrim.md) | 2 |
| [TruncateText](A03/TruncateText.md) | 1 |

## A04 逻辑分支与执行路径

| 节点 | 用例数 |
|---|---|
| [ComfyAndNode](A04/ComfyAndNode.md) | 1 |
| [ComfySwitchNode](A04/ComfySwitchNode.md) | 1 |
| [ComfyNotNode](A04/ComfyNotNode.md) | 1 |
| [ComfyOrNode](A04/ComfyOrNode.md) | 1 |

## A05 图像空间变换

| 节点 | 用例数 |
|---|---|
| [ImageCropV2](A05/ImageCropV2.md) | 2 |
| [CenterCropImages](A05/CenterCropImages.md) | 2 |
| [ImageCrop](A05/ImageCrop.md) | 2 |
| [RandomCropImages](A05/RandomCropImages.md) | 2 |
| [ImageCropToMask](A05/ImageCropToMask.md) | 2 |
| [ImageFlip](A05/ImageFlip.md) | 1 |
| [ImagePadForOutpaint](A05/ImagePadForOutpaint.md) | 2 |
| [ResizeAndPadImage](A05/ResizeAndPadImage.md) | 1 |
| [ResizeImageMaskNode](A05/ResizeImageMaskNode.md) | 2 |
| [ResizeImagesByLongerEdge](A05/ResizeImagesByLongerEdge.md) | 1 |
| [ResizeImagesByShorterEdge](A05/ResizeImagesByShorterEdge.md) | 1 |
| [ImageRotate](A05/ImageRotate.md) | 1 |
| [ImageStitch](A05/ImageStitch.md) | 2 |
| [ImageScaleToMaxDimension](A05/ImageScaleToMaxDimension.md) | 1 |
| [ImageScaleToTotalPixels](A05/ImageScaleToTotalPixels.md) | 1 |
| [ImageScale](A05/ImageScale.md) | 3 |
| [ImageScaleBy](A05/ImageScaleBy.md) | 1 |

## A06 图像颜色与滤波

| 节点 | 用例数 |
|---|---|
| [AdjustBrightness](A06/AdjustBrightness.md) | 3 |
| [AdjustContrast](A06/AdjustContrast.md) | 2 |
| [ImageRGBToYUV](A06/ImageRGBToYUV.md) | 2 |
| [ImageYUVToRGB](A06/ImageYUVToRGB.md) | 2 |
| [ImageInvert](A06/ImageInvert.md) | 2 |
| [NormalizeImages](A06/NormalizeImages.md) | 2 |
| [ImageAddNoise](A06/ImageAddNoise.md) | 2 |
| [Morphology](A06/Morphology.md) | 2 |
| [ImageBlend](A06/ImageBlend.md) | 2 |
| [ImageBlur](A06/ImageBlur.md) | 2 |
| [Canny](A06/Canny.md) | 2 |
| [ImageQuantize](A06/ImageQuantize.md) | 2 |
| [ImageSharpen](A06/ImageSharpen.md) | 2 |
| [ColorTransfer](A06/ColorTransfer.md) | 1 |
| [ImageHistogram](A06/ImageHistogram.md) | 1 |

## A07 遮罩数值与空间范围

| 节点 | 用例数 |
|---|---|
| [LoadImageMask](A07/LoadImageMask.md) | 2 |
| [BatchMasksNode](A07/BatchMasksNode.md) | 2 |
| [MaskComposite](A07/MaskComposite.md) | 1 |
| [ImageColorToMask](A07/ImageColorToMask.md) | 1 |
| [ImageToMask](A07/ImageToMask.md) | 2 |
| [MaskToImage](A07/MaskToImage.md) | 1 |
| [SolidMask](A07/SolidMask.md) | 2 |
| [CropMask](A07/CropMask.md) | 1 |
| [FeatherMask](A07/FeatherMask.md) | 2 |
| [GrowMask](A07/GrowMask.md) | 2 |
| [InvertMask](A07/InvertMask.md) | 2 |
| [MaskPreview](A07/MaskPreview.md) | 1 |
| [ThresholdMask](A07/ThresholdMask.md) | 2 |

## A08 遮罩合成与透明通道

| 节点 | 用例数 |
|---|---|
| [ImageCompositeMasked](A08/ImageCompositeMasked.md) | 2 |
| [JoinImageWithAlpha](A08/JoinImageWithAlpha.md) | 2 |
| [PorterDuffImageComposite](A08/PorterDuffImageComposite.md) | 2 |
| [SplitImageWithAlpha](A08/SplitImageWithAlpha.md) | 2 |

## A09 批次 列表与分块

| 节点 | 用例数 |
|---|---|
| [BatchImagesNode](A09/BatchImagesNode.md) | 2 |
| [ImageBatch](A09/ImageBatch.md) | 2 |
| [ImageDeduplication](A09/ImageDeduplication.md) | 2 |
| [ImageFromBatch](A09/ImageFromBatch.md) | 2 |
| [ImageGrid](A09/ImageGrid.md) | 1 |
| [MergeImageLists](A09/MergeImageLists.md) | 2 |
| [ImageMergeTileList](A09/ImageMergeTileList.md) | 2 |
| [RebatchImages](A09/RebatchImages.md) | 1 |
| [RepeatImageBatch](A09/RepeatImageBatch.md) | 1 |
| [SplitImageToTileList](A09/SplitImageToTileList.md) | 2 |

## A10 边界框与图层

| 节点 | 用例数 |
|---|---|
| [AddLayer](A10/AddLayer.md) | 2 |
| [ImageCompositor](A10/ImageCompositor.md) | 2 |
| [LayersFromBoundingBoxes](A10/LayersFromBoundingBoxes.md) | 2 |
| [DrawBBoxes](A10/DrawBBoxes.md) | 2 |
| [CropByBBoxes](A10/CropByBBoxes.md) | 2 |
| [CreateBoundingBoxes](A10/CreateBoundingBoxes.md) | 2 |
| [PrimitiveBoundingBox](A10/PrimitiveBoundingBox.md) | 2 |

## A11 图像来源与导出格式

| 节点 | 用例数 |
|---|---|
| [EmptyImage](A11/EmptyImage.md) | 2 |
| [Painter](A11/Painter.md) | 2 |
| [SaveAnimatedPNG](A11/SaveAnimatedPNG.md) | 2 |
| [SaveAnimatedWEBP](A11/SaveAnimatedWEBP.md) | 2 |
| [SaveImageAdvanced](A11/SaveImageAdvanced.md) | 2 |
| [SaveSVGNode](A11/SaveSVGNode.md) | 2 |
| [WebcamCapture](A11/WebcamCapture.md) | 2 |

## A12 图文数据集配对

| 节点 | 用例数 |
|---|---|
| [LoadImageDataSetFromFolder](A12/LoadImageDataSetFromFolder.md) | 2 |
| [LoadImageTextDataSetFromFolder](A12/LoadImageTextDataSetFromFolder.md) | 2 |
| [SaveImageDataSetToFolder](A12/SaveImageDataSetToFolder.md) | 2 |
| [SaveImageTextDataSetToFolder](A12/SaveImageTextDataSetToFolder.md) | 2 |
| [ShuffleDataset](A12/ShuffleDataset.md) | 2 |
| [ShuffleImageTextDataset](A12/ShuffleImageTextDataset.md) | 2 |

## A13 图像着色器

| 节点 | 用例数 |
|---|---|
| [GLSLShader](A13/GLSLShader.md) | 2 |

## B01 加载器与最小条件编码

| 节点 | 用例数 |
|---|---|
| [CLIPSetLastLayer](B01/CLIPSetLastLayer.md) | 3 |
| [CLIPTextEncode](B01/CLIPTextEncode.md) | 2 |
| [T5TokenizerOptions](B01/T5TokenizerOptions.md) | 3 |
| [CheckpointLoaderSimple](B01/CheckpointLoaderSimple.md) | 2 |
| [ImageOnlyCheckpointLoader](B01/ImageOnlyCheckpointLoader.md) | 2 |
| [CheckpointLoader](B01/CheckpointLoader.md) | 2 |
| [CLIPLoader](B01/CLIPLoader.md) | 3 |
| [DualCLIPLoader](B01/DualCLIPLoader.md) | 3 |
| [QuadrupleCLIPLoader](B01/QuadrupleCLIPLoader.md) | 2 |
| [TripleCLIPLoader](B01/TripleCLIPLoader.md) | 2 |
| [DiffusersLoader](B01/DiffusersLoader.md) | 2 |
| [UNETLoader](B01/UNETLoader.md) | 3 |
| [VAELoader](B01/VAELoader.md) | 2 |

## B02 像素与潜空间往返

| 节点 | 用例数 |
|---|---|
| [VAEDecode](B02/VAEDecode.md) | 2 |
| [VAEDecodeTiled](B02/VAEDecodeTiled.md) | 2 |
| [VAEEncode](B02/VAEEncode.md) | 2 |
| [VAEEncodeTiled](B02/VAEEncodeTiled.md) | 2 |

## B03 最小文生图与复现

| 节点 | 用例数 |
|---|---|
| [EmptyLatentImage](B03/EmptyLatentImage.md) | 2 |
| [KSampler](B03/KSampler.md) | 4 |

## B04 图生图与去噪强度

| 节点 | 用例数 |
|---|---|
| [KSamplerAdvanced](B04/KSamplerAdvanced.md) | 2 |

## B05 局部重绘与外扩

| 节点 | 用例数 |
|---|---|
| [InpaintModelConditioning](B05/InpaintModelConditioning.md) | 2 |
| [SetLatentNoiseMask](B05/SetLatentNoiseMask.md) | 2 |
| [VAEEncodeForInpaint](B05/VAEEncodeForInpaint.md) | 2 |

## B06 潜空间操作与保存

| 节点 | 用例数 |
|---|---|
| [LatentBlend](B06/LatentBlend.md) | 2 |
| [LatentComposite](B06/LatentComposite.md) | 2 |
| [LatentCompositeMasked](B06/LatentCompositeMasked.md) | 2 |
| [LoadLatent](B06/LoadLatent.md) | 2 |
| [SaveLatent](B06/SaveLatent.md) | 2 |
| [LatentUpscale](B06/LatentUpscale.md) | 2 |
| [LatentUpscaleBy](B06/LatentUpscaleBy.md) | 2 |
| [LatentAdd](B06/LatentAdd.md) | 2 |
| [LatentBatchSeedBehavior](B06/LatentBatchSeedBehavior.md) | 1 |
| [LatentConcat](B06/LatentConcat.md) | 2 |
| [LatentCut](B06/LatentCut.md) | 2 |
| [LatentCutToBatch](B06/LatentCutToBatch.md) | 2 |
| [LatentInterpolate](B06/LatentInterpolate.md) | 2 |
| [LatentMultiply](B06/LatentMultiply.md) | 2 |
| [LatentSubtract](B06/LatentSubtract.md) | 2 |
| [LatentApplyOperation](B06/LatentApplyOperation.md) | 2 |
| [LatentApplyOperationCFG](B06/LatentApplyOperationCFG.md) | 2 |
| [LatentOperationSharpen](B06/LatentOperationSharpen.md) | 2 |
| [LatentOperationTonemapReinhard](B06/LatentOperationTonemapReinhard.md) | 2 |
| [BatchLatentsNode](B06/BatchLatentsNode.md) | 2 |
| [LatentBatch](B06/LatentBatch.md) | 2 |
| [LatentFromBatch](B06/LatentFromBatch.md) | 2 |
| [RebatchLatents](B06/RebatchLatents.md) | 1 |
| [RepeatLatentBatch](B06/RepeatLatentBatch.md) | 1 |
| [LatentCrop](B06/LatentCrop.md) | 2 |
| [LatentFlip](B06/LatentFlip.md) | 1 |
| [LatentRotate](B06/LatentRotate.md) | 1 |

## B07 拆开采样器

| 节点 | 用例数 |
|---|---|
| [SamplerCustom](B07/SamplerCustom.md) | 2 |
| [SamplerCustomAdvanced](B07/SamplerCustomAdvanced.md) | 2 |
| [BasicGuider](B07/BasicGuider.md) | 2 |
| [CFGGuider](B07/CFGGuider.md) | 2 |
| [AddNoise](B07/AddNoise.md) | 2 |
| [DisableNoise](B07/DisableNoise.md) | 2 |
| [RandomNoise](B07/RandomNoise.md) | 2 |
| [KSamplerSelect](B07/KSamplerSelect.md) | 1 |
| [BasicScheduler](B07/BasicScheduler.md) | 3 |

## B08 噪声时间表与分段采样

| 节点 | 用例数 |
|---|---|
| [AlignYourStepsScheduler](B08/AlignYourStepsScheduler.md) | 3 |
| [BetaSamplingScheduler](B08/BetaSamplingScheduler.md) | 3 |
| [ExponentialScheduler](B08/ExponentialScheduler.md) | 3 |
| [GITSScheduler](B08/GITSScheduler.md) | 3 |
| [KarrasScheduler](B08/KarrasScheduler.md) | 2 |
| [LaplaceScheduler](B08/LaplaceScheduler.md) | 3 |
| [OptimalStepsScheduler](B08/OptimalStepsScheduler.md) | 3 |
| [PolyexponentialScheduler](B08/PolyexponentialScheduler.md) | 4 |
| [SDTurboScheduler](B08/SDTurboScheduler.md) | 3 |
| [VPScheduler](B08/VPScheduler.md) | 3 |
| [ExtendIntermediateSigmas](B08/ExtendIntermediateSigmas.md) | 2 |
| [FlipSigmas](B08/FlipSigmas.md) | 2 |
| [ManualSigmas](B08/ManualSigmas.md) | 2 |
| [SamplingPercentToSigma](B08/SamplingPercentToSigma.md) | 2 |
| [SetFirstSigma](B08/SetFirstSigma.md) | 2 |
| [SplitSigmas](B08/SplitSigmas.md) | 2 |
| [SplitSigmasDenoise](B08/SplitSigmasDenoise.md) | 2 |

## B09 采样算法的替换

| 节点 | 用例数 |
|---|---|
| [SamplerEulerCFGpp](B09/SamplerEulerCFGpp.md) | 2 |
| [SamplerDPMAdaptative](B09/SamplerDPMAdaptative.md) | 4 |
| [SamplerDPMPP_2M_SDE](B09/SamplerDPMPP_2M_SDE.md) | 4 |
| [SamplerDPMPP_2S_Ancestral](B09/SamplerDPMPP_2S_Ancestral.md) | 4 |
| [SamplerDPMPP_3M_SDE](B09/SamplerDPMPP_3M_SDE.md) | 4 |
| [SamplerDPMPP_SDE](B09/SamplerDPMPP_SDE.md) | 4 |
| [SamplerER_SDE](B09/SamplerER_SDE.md) | 4 |
| [SamplerEulerAncestral](B09/SamplerEulerAncestral.md) | 4 |
| [SamplerEulerAncestralCFGPP](B09/SamplerEulerAncestralCFGPP.md) | 4 |
| [SamplerLCM](B09/SamplerLCM.md) | 3 |
| [SamplerLCMUpscale](B09/SamplerLCMUpscale.md) | 2 |
| [SamplerLMS](B09/SamplerLMS.md) | 2 |
| [SamplerSASolver](B09/SamplerSASolver.md) | 4 |
| [SamplerSEEDS2](B09/SamplerSEEDS2.md) | 4 |

## B10 引导器与引导补丁

| 节点 | 用例数 |
|---|---|
| [CFGNorm](B10/CFGNorm.md) | 3 |
| [CFGZeroStar](B10/CFGZeroStar.md) | 2 |
| [LTXVModalityGuidance](B10/LTXVModalityGuidance.md) | 4 |
| [LTXVSpatioTemporalGuidance](B10/LTXVSpatioTemporalGuidance.md) | 5 |
| [NAGuidance](B10/NAGuidance.md) | 2 |
| [SkipLayerGuidanceDiT](B10/SkipLayerGuidanceDiT.md) | 5 |
| [SkipLayerGuidanceDiTSimple](B10/SkipLayerGuidanceDiTSimple.md) | 4 |
| [SkipLayerGuidanceSD3](B10/SkipLayerGuidanceSD3.md) | 5 |
| [TCFG](B10/TCFG.md) | 2 |
| [FreSca](B10/FreSca.md) | 2 |
| [PerpNeg](B10/PerpNeg.md) | 2 |
| [PerpNegGuider](B10/PerpNegGuider.md) | 3 |
| [Mahiro](B10/Mahiro.md) | 2 |
| [SelfAttentionGuidance](B10/SelfAttentionGuidance.md) | 3 |
| [APG](B10/APG.md) | 3 |
| [CFGOverride](B10/CFGOverride.md) | 2 |
| [DualCFGGuider](B10/DualCFGGuider.md) | 2 |
| [DualModelGuider](B10/DualModelGuider.md) | 3 |
| [LTXVDualCFGGuider](B10/LTXVDualCFGGuider.md) | 2 |
| [VideoLinearCFGGuidance](B10/VideoLinearCFGGuidance.md) | 2 |
| [VideoTriangleCFGGuidance](B10/VideoTriangleCFGGuidance.md) | 2 |

## B11 条件组合 区域与时段

| 节点 | 用例数 |
|---|---|
| [ConditioningTimestepsRange](B11/ConditioningTimestepsRange.md) | 2 |
| [ConditioningAverage](B11/ConditioningAverage.md) | 2 |
| [ConditioningCombine](B11/ConditioningCombine.md) | 2 |
| [ConditioningConcat](B11/ConditioningConcat.md) | 2 |
| [ConditioningMultiply](B11/ConditioningMultiply.md) | 2 |
| [ConditioningSetAreaStrength](B11/ConditioningSetAreaStrength.md) | 2 |
| [ConditioningSetAreaPercentageVideo](B11/ConditioningSetAreaPercentageVideo.md) | 2 |
| [ConditioningSetAreaPercentage](B11/ConditioningSetAreaPercentage.md) | 2 |
| [ConditioningSetArea](B11/ConditioningSetArea.md) | 2 |
| [ConditioningSetMask](B11/ConditioningSetMask.md) | 2 |
| [ConditioningZeroOut](B11/ConditioningZeroOut.md) | 2 |
| [ConditioningSetTimestepRange](B11/ConditioningSetTimestepRange.md) | 2 |

## B12 LoRA 与旁路

| 节点 | 用例数 |
|---|---|
| [LoraLoaderModelOnly](B12/LoraLoaderModelOnly.md) | 2 |
| [LoraLoaderBypass](B12/LoraLoaderBypass.md) | 2 |
| [LoraLoaderBypassModelOnly](B12/LoraLoaderBypassModelOnly.md) | 2 |
| [LoraLoader](B12/LoraLoader.md) | 2 |
| [LoraModelLoader](B12/LoraModelLoader.md) | 2 |

## B13 ControlNet 与结构条件

| 节点 | 用例数 |
|---|---|
| [CLIPTextEncodeControlnet](B13/CLIPTextEncodeControlnet.md) | 2 |
| [ControlNetApplyAdvanced](B13/ControlNetApplyAdvanced.md) | 6 |
| [ControlNetApply](B13/ControlNetApply.md) | 4 |
| [ControlNetInpaintingAliMamaApply](B13/ControlNetInpaintingAliMamaApply.md) | 6 |
| [ControlNetApplySD3](B13/ControlNetApplySD3.md) | 6 |
| [SetUnionControlNetType](B13/SetUnionControlNetType.md) | 2 |
| [ControlNetLoader](B13/ControlNetLoader.md) | 2 |
| [DiffControlNetLoader](B13/DiffControlNetLoader.md) | 2 |

## B14 图像编码与风格身份条件

| 节点 | 用例数 |
|---|---|
| [StyleModelApply](B14/StyleModelApply.md) | 4 |
| [CLIPVisionEncode](B14/CLIPVisionEncode.md) | 2 |
| [ReferenceLatent](B14/ReferenceLatent.md) | 2 |
| [unCLIPConditioning](B14/unCLIPConditioning.md) | 4 |
| [GLIGENTextBoxApply](B14/GLIGENTextBoxApply.md) | 3 |
| [PhotoMakerEncode](B14/PhotoMakerEncode.md) | 2 |
| [CLIPVisionLoader](B14/CLIPVisionLoader.md) | 2 |
| [GLIGENLoader](B14/GLIGENLoader.md) | 2 |
| [PhotoMakerLoader](B14/PhotoMakerLoader.md) | 2 |
| [StyleModelLoader](B14/StyleModelLoader.md) | 2 |
| [unCLIPCheckpointLoader](B14/unCLIPCheckpointLoader.md) | 2 |

## C01 视频拆分与封装

| 节点 | 用例数 |
|---|---|
| [CreateVideo](C01/CreateVideo.md) | 2 |
| [GetVideoComponents](C01/GetVideoComponents.md) | 2 |
| [LoadVideo](C01/LoadVideo.md) | 2 |
| [SaveVideo](C01/SaveVideo.md) | 2 |
| [SaveWEBM](C01/SaveWEBM.md) | 2 |

## C02 视频时间裁剪与潜空间帧

| 节点 | 用例数 |
|---|---|
| [TrimVideoLatent](C02/TrimVideoLatent.md) | 2 |
| [ReplaceVideoLatentFrames](C02/ReplaceVideoLatentFrames.md) | 2 |
| [VideoFrameSample](C02/VideoFrameSample.md) | 2 |
| [Video Slice](C02/Video_20Slice.md) | 2 |
| [VideoRandomTemporalCrop](C02/VideoRandomTemporalCrop.md) | 2 |
| [VideoTemporalCrop](C02/VideoTemporalCrop.md) | 2 |

## C03 音频通道 时间与封装

| 节点 | 用例数 |
|---|---|
| [AudioAdjustVolume](C03/AudioAdjustVolume.md) | 2 |
| [AudioEqualizer3Band](C03/AudioEqualizer3Band.md) | 2 |
| [AudioConcat](C03/AudioConcat.md) | 1 |
| [EmptyAudio](C03/EmptyAudio.md) | 2 |
| [JoinAudioChannels](C03/JoinAudioChannels.md) | 2 |
| [LoadAudio](C03/LoadAudio.md) | 2 |
| [AudioMerge](C03/AudioMerge.md) | 2 |
| [PreviewAudio](C03/PreviewAudio.md) | 2 |
| [RecordAudio](C03/RecordAudio.md) | 2 |
| [SaveAudioAdvanced](C03/SaveAudioAdvanced.md) | 2 |
| [SaveAudio](C03/SaveAudio.md) | 2 |
| [SaveAudioMP3](C03/SaveAudioMP3.md) | 2 |
| [SaveAudioOpus](C03/SaveAudioOpus.md) | 2 |
| [SplitAudioChannels](C03/SplitAudioChannels.md) | 2 |
| [TrimAudioDuration](C03/TrimAudioDuration.md) | 2 |

## C04 学习型放大与插帧

| 节点 | 用例数 |
|---|---|
| [ImageUpscaleWithModel](C04/ImageUpscaleWithModel.md) | 2 |
| [FrameInterpolationModelLoader](C04/FrameInterpolationModelLoader.md) | 2 |
| [LatentUpscaleModelLoader](C04/LatentUpscaleModelLoader.md) | 2 |
| [UpscaleModelLoader](C04/UpscaleModelLoader.md) | 2 |
| [FrameInterpolate](C04/FrameInterpolate.md) | 2 |

## C05 视频与图文数据集

| 节点 | 用例数 |
|---|---|
| [ShuffleVideoTextDataset](C05/ShuffleVideoTextDataset.md) | 2 |
| [LoadVideoDataSetFromFolder](C05/LoadVideoDataSetFromFolder.md) | 2 |
| [LoadVideoTextDataSetFromFolder](C05/LoadVideoTextDataSetFromFolder.md) | 2 |
| [ShuffleVideoDataset](C05/ShuffleVideoDataset.md) | 2 |

## D01 H3 参考视频最小闭环

| 节点 | 用例数 |
|---|---|
| [MiniMaxH3ReferenceToVideo](D01/MiniMaxH3ReferenceToVideo.md) | 4 |
| [VAEDecodeAudio](D01/VAEDecodeAudio.md) | 2 |
| [VAEDecodeAudioTiled](D01/VAEDecodeAudioTiled.md) | 2 |

## D02 H3 首末帧与时长网格

| 节点 | 用例数 |
|---|---|
| [MiniMaxH3ImageToVideo](D02/MiniMaxH3ImageToVideo.md) | 2 |
| [EmptyMiniMaxH3LatentAV](D02/EmptyMiniMaxH3LatentAV.md) | 2 |

## D03 H3 时间锚点与多参考

| 节点 | 用例数 |
|---|---|
| [MiniMaxH3AddGuide](D03/MiniMaxH3AddGuide.md) | 2 |

## D04 H3 视频与音频采样偏移

| 节点 | 用例数 |
|---|---|
| [MiniMaxH3SigmaShift](D04/MiniMaxH3SigmaShift.md) | 1 |

## F01 三维文件 相机与预览

| 节点 | 用例数 |
|---|---|
| [CreateCameraInfo](F01/CreateCameraInfo.md) | 3 |
| [Load3D](F01/Load3D.md) | 2 |
| [Load3DAdvanced](F01/Load3DAdvanced.md) | 2 |
| [Preview3D](F01/Preview3D.md) | 2 |
| [Preview3DAdvanced](F01/Preview3DAdvanced.md) | 2 |
| [PreviewPointCloud](F01/PreviewPointCloud.md) | 2 |
| [Save3DAdvanced](F01/Save3DAdvanced.md) | 2 |
| [SaveGLB](F01/SaveGLB.md) | 2 |
| [SavePointCloud](F01/SavePointCloud.md) | 2 |

## F02 图像几何估计与网格

| 节点 | 用例数 |
|---|---|
| [DA3GeometryToMesh](F02/DA3GeometryToMesh.md) | 2 |
| [MoGePointMapToMesh](F02/MoGePointMapToMesh.md) | 2 |
| [MoGeGeometryToFOV](F02/MoGeGeometryToFOV.md) | 1 |
| [DA3Render](F02/DA3Render.md) | 1 |
| [MoGeRender](F02/MoGeRender.md) | 1 |
| [DA3Inference](F02/DA3Inference.md) | 2 |
| [MoGeInference](F02/MoGeInference.md) | 2 |
| [MoGePanoramaInference](F02/MoGePanoramaInference.md) | 2 |
| [LoadDA3Model](F02/LoadDA3Model.md) | 3 |
| [LoadMoGeModel](F02/LoadMoGeModel.md) | 2 |

## F03 网格后处理与文件转换

| 节点 | 用例数 |
|---|---|
| [MeshToFile3D](F03/MeshToFile3D.md) | 2 |
| [DecimateMesh](F03/DecimateMesh.md) | 2 |
| [FillHoles](F03/FillHoles.md) | 2 |
| [GetMeshInfo](F03/GetMeshInfo.md) | 1 |
| [MergeMeshes](F03/MergeMeshes.md) | 2 |
| [PaintMesh](F03/PaintMesh.md) | 2 |
| [RemeshMesh](F03/RemeshMesh.md) | 2 |
| [RenderMesh](F03/RenderMesh.md) | 2 |
| [RotateMesh](F03/RotateMesh.md) | 2 |
| [MeshSmoothNormals](F03/MeshSmoothNormals.md) | 1 |
| [WeldVertices](F03/WeldVertices.md) | 2 |

## F04 UV 贴图与烘焙

| 节点 | 用例数 |
|---|---|
| [ApplyTextureToMesh](F04/ApplyTextureToMesh.md) | 2 |
| [BakeAmbientOcclusion](F04/BakeAmbientOcclusion.md) | 2 |
| [BakeNormalMapFromMesh](F04/BakeNormalMapFromMesh.md) | 2 |
| [BakeTextureFromVoxel](F04/BakeTextureFromVoxel.md) | 2 |
| [MeshTextureToImage](F04/MeshTextureToImage.md) | 2 |
| [RenderUVAtlas](F04/RenderUVAtlas.md) | 2 |
| [UnwrapMesh](F04/UnwrapMesh.md) | 2 |

## F05 Splat 数据 文件与渲染

| 节点 | 用例数 |
|---|---|
| [PreviewGaussianSplat](F05/PreviewGaussianSplat.md) | 2 |
| [SaveGaussianSplat](F05/SaveGaussianSplat.md) | 2 |
| [SplatToFile3D](F05/SplatToFile3D.md) | 2 |
| [SplatToMesh](F05/SplatToMesh.md) | 2 |
| [File3DToSplat](F05/File3DToSplat.md) | 2 |
| [GetSplatCount](F05/GetSplatCount.md) | 1 |
| [MergeSplat](F05/MergeSplat.md) | 1 |
| [RenderSplat](F05/RenderSplat.md) | 2 |
| [TransformSplat](F05/TransformSplat.md) | 2 |

## F06 目标检测与自动遮罩

| 节点 | 用例数 |
|---|---|
| [RemoveBackground](F06/RemoveBackground.md) | 1 |
| [RTDETR_detect](F06/RTDETR_detect.md) | 2 |
| [SAM3_Detect](F06/SAM3_Detect.md) | 2 |
| [LoadBackgroundRemovalModel](F06/LoadBackgroundRemovalModel.md) | 2 |

## F07 视频目标跟踪

| 节点 | 用例数 |
|---|---|
| [SAM3_VideoTrack](F07/SAM3_VideoTrack.md) | 2 |
| [SAM3_TrackPreview](F07/SAM3_TrackPreview.md) | 2 |
| [SAM3_TrackToMask](F07/SAM3_TrackToMask.md) | 2 |

## F08 SAM3D 人体姿态预测

| 节点 | 用例数 |
|---|---|
| [SAM3DBody_Loader](F08/SAM3DBody_Loader.md) | 2 |
| [SAM3DBody_Render](F08/SAM3DBody_Render.md) | 2 |
| [SAM3DBody_Predict](F08/SAM3DBody_Predict.md) | 2 |

## F09 姿态时序平滑

| 节点 | 用例数 |
|---|---|
| [SAM3DBody_Smooth](F09/SAM3DBody_Smooth.md) | 2 |

## F10 人体动画导出

| 节点 | 用例数 |
|---|---|
| [BuildPoseFile](F10/BuildPoseFile.md) | 6 |

## F11 人脸关键点与人体表情

| 节点 | 用例数 |
|---|---|
| [MediaPipeFaceLandmarker](F11/MediaPipeFaceLandmarker.md) | 2 |
| [MediaPipeFaceMask](F11/MediaPipeFaceMask.md) | 2 |
| [SAM3DBody_FaceExpression](F11/SAM3DBody_FaceExpression.md) | 2 |
| [MediaPipeFaceMeshVisualize](F11/MediaPipeFaceMeshVisualize.md) | 2 |
| [LoadMediaPipeFaceLandmarker](F11/LoadMediaPipeFaceLandmarker.md) | 2 |

## F12 二维姿态与关键点表示

| 节点 | 用例数 |
|---|---|
| [SDPoseDrawKeypoints](F12/SDPoseDrawKeypoints.md) | 2 |
| [SDPoseFaceBBoxes](F12/SDPoseFaceBBoxes.md) | 2 |
| [SDPoseKeypointExtractor](F12/SDPoseKeypointExtractor.md) | 2 |

## G01 模型补丁与注意力实验

| 节点 | 用例数 |
|---|---|
| [CLIPAttentionMultiply](G01/CLIPAttentionMultiply.md) | 2 |
| [UNetCrossAttentionMultiply](G01/UNetCrossAttentionMultiply.md) | 2 |
| [UNetSelfAttentionMultiply](G01/UNetSelfAttentionMultiply.md) | 2 |
| [UNetTemporalAttentionMultiply](G01/UNetTemporalAttentionMultiply.md) | 2 |
| [ContextWindowsManual](G01/ContextWindowsManual.md) | 2 |
| [LTXVContextWindows](G01/LTXVContextWindows.md) | 2 |
| [ModelAttentionBackend](G01/ModelAttentionBackend.md) | 2 |
| [ModelNoiseScale](G01/ModelNoiseScale.md) | 2 |
| [ModelSamplingAuraFlow](G01/ModelSamplingAuraFlow.md) | 3 |
| [ModelSamplingContinuousEDM](G01/ModelSamplingContinuousEDM.md) | 2 |
| [ModelSamplingContinuousV](G01/ModelSamplingContinuousV.md) | 2 |
| [ModelSamplingDiscrete](G01/ModelSamplingDiscrete.md) | 2 |
| [RenormCFG](G01/RenormCFG.md) | 2 |
| [RescaleCFG](G01/RescaleCFG.md) | 3 |
| [ScaleROPE](G01/ScaleROPE.md) | 2 |
| [WanContextWindowsManual](G01/WanContextWindowsManual.md) | 2 |
| [ChromaRadianceOptions](G01/ChromaRadianceOptions.md) | 2 |
| [ModelSamplingFlux](G01/ModelSamplingFlux.md) | 3 |
| [HiDreamO1PatchSeamSmoothing](G01/HiDreamO1PatchSeamSmoothing.md) | 5 |
| [ModelSamplingLTXV](G01/ModelSamplingLTXV.md) | 2 |
| [ModelSamplingStableCascade](G01/ModelSamplingStableCascade.md) | 3 |
| [ModelSamplingSD3](G01/ModelSamplingSD3.md) | 3 |
| [Epsilon Scaling](G01/Epsilon_20Scaling.md) | 2 |
| [FreeU](G01/FreeU.md) | 2 |
| [FreeU_V2](G01/FreeU_V2.md) | 2 |
| [HyperTile](G01/HyperTile.md) | 2 |
| [PatchModelAddDownscale](G01/PatchModelAddDownscale.md) | 4 |
| [PerturbedAttentionGuidance](G01/PerturbedAttentionGuidance.md) | 3 |
| [TomePatchModel](G01/TomePatchModel.md) | 2 |
| [TemporalScoreRescaling](G01/TemporalScoreRescaling.md) | 2 |

## G02 Hook 的时间控制与组合

| 节点 | 用例数 |
|---|---|
| [SetClipHooks](G02/SetClipHooks.md) | 2 |
| [CombineHooks2](G02/CombineHooks2.md) | 2 |
| [CombineHooks4](G02/CombineHooks4.md) | 2 |
| [CombineHooks8](G02/CombineHooks8.md) | 2 |
| [PairConditioningCombine](G02/PairConditioningCombine.md) | 2 |
| [PairConditioningSetDefaultCombine](G02/PairConditioningSetDefaultCombine.md) | 2 |
| [PairConditioningSetProperties](G02/PairConditioningSetProperties.md) | 3 |
| [PairConditioningSetPropertiesAndCombine](G02/PairConditioningSetPropertiesAndCombine.md) | 3 |
| [ConditioningSetDefaultCombine](G02/ConditioningSetDefaultCombine.md) | 2 |
| [ConditioningSetProperties](G02/ConditioningSetProperties.md) | 3 |
| [ConditioningSetPropertiesAndCombine](G02/ConditioningSetPropertiesAndCombine.md) | 3 |
| [CreateHookLora](G02/CreateHookLora.md) | 3 |
| [CreateHookLoraModelOnly](G02/CreateHookLoraModelOnly.md) | 3 |
| [CreateHookModelAsLora](G02/CreateHookModelAsLora.md) | 3 |
| [CreateHookModelAsLoraModelOnly](G02/CreateHookModelAsLoraModelOnly.md) | 3 |
| [CreateHookKeyframe](G02/CreateHookKeyframe.md) | 2 |
| [CreateHookKeyframesFromFloats](G02/CreateHookKeyframesFromFloats.md) | 2 |
| [CreateHookKeyframesInterpolated](G02/CreateHookKeyframesInterpolated.md) | 2 |
| [SetHookKeyframes](G02/SetHookKeyframes.md) | 2 |

## G03 模型合并与保存回读

| 节点 | 用例数 |
|---|---|
| [LoraSave](G03/LoraSave.md) | 2 |
| [CLIPMergeAdd](G03/CLIPMergeAdd.md) | 2 |
| [CLIPMergeSimple](G03/CLIPMergeSimple.md) | 2 |
| [CLIPMergeSubtract](G03/CLIPMergeSubtract.md) | 3 |
| [CLIPSave](G03/CLIPSave.md) | 2 |
| [ImageOnlyCheckpointSave](G03/ImageOnlyCheckpointSave.md) | 2 |
| [ModelMergeAdd](G03/ModelMergeAdd.md) | 2 |
| [ModelMergeBlocks](G03/ModelMergeBlocks.md) | 2 |
| [ModelMergeSimple](G03/ModelMergeSimple.md) | 2 |
| [ModelMergeSubtract](G03/ModelMergeSubtract.md) | 3 |
| [ModelSave](G03/ModelSave.md) | 2 |
| [CheckpointSave](G03/CheckpointSave.md) | 2 |
| [SaveLoRA](G03/SaveLoRA.md) | 2 |
| [VAESave](G03/VAESave.md) | 2 |
| [ModelMergeAuraflow](G03/ModelMergeAuraflow.md) | 2 |
| [ModelMergeCosmos14B](G03/ModelMergeCosmos14B.md) | 2 |
| [ModelMergeCosmos7B](G03/ModelMergeCosmos7B.md) | 2 |
| [ModelMergeCosmosPredict2_14B](G03/ModelMergeCosmosPredict2_14B.md) | 2 |
| [ModelMergeCosmosPredict2_2B](G03/ModelMergeCosmosPredict2_2B.md) | 2 |
| [ModelMergeFlux1](G03/ModelMergeFlux1.md) | 2 |
| [ModelMergeKrea2](G03/ModelMergeKrea2.md) | 2 |
| [ModelMergeLTXV](G03/ModelMergeLTXV.md) | 2 |
| [ModelMergeMochiPreview](G03/ModelMergeMochiPreview.md) | 2 |
| [ModelMergeQwenImage](G03/ModelMergeQwenImage.md) | 2 |
| [ModelMergeSD1](G03/ModelMergeSD1.md) | 2 |
| [ModelMergeSD2](G03/ModelMergeSD2.md) | 2 |
| [ModelMergeSD35_Large](G03/ModelMergeSD35_Large.md) | 2 |
| [ModelMergeSD3_2B](G03/ModelMergeSD3_2B.md) | 2 |
| [ModelMergeSDXL](G03/ModelMergeSDXL.md) | 2 |
| [ModelMergeWAN2_1](G03/ModelMergeWAN2_1.md) | 2 |

## G04 性能 缓存与设备

| 节点 | 用例数 |
|---|---|
| [EasyCache](G04/EasyCache.md) | 5 |
| [LazyCache](G04/LazyCache.md) | 5 |
| [ModelComputeDtype](G04/ModelComputeDtype.md) | 2 |
| [MultiGPU_WorkUnits](G04/MultiGPU_WorkUnits.md) | 3 |
| [SelectCLIPDevice](G04/SelectCLIPDevice.md) | 2 |
| [SelectModelDevice](G04/SelectModelDevice.md) | 2 |
| [SelectVAEDevice](G04/SelectVAEDevice.md) | 2 |
| [FluxKVCache](G04/FluxKVCache.md) | 2 |
| [TorchCompileModel](G04/TorchCompileModel.md) | 2 |

## G05 训练数据与最小 LoRA 训练

| 节点 | 用例数 |
|---|---|
| [LoadTrainingDataset](G05/LoadTrainingDataset.md) | 2 |
| [MakeTrainingDataset](G05/MakeTrainingDataset.md) | 2 |
| [LossGraphNode](G05/LossGraphNode.md) | 2 |
| [ResolutionBucket](G05/ResolutionBucket.md) | 2 |
| [SaveTrainingDataset](G05/SaveTrainingDataset.md) | 2 |
| [TrainLoraNode](G05/TrainLoraNode.md) | 3 |

## G06 弃用占位节点兼容性

| 节点 | 用例数 |
|---|---|
| [wanBlockSwap](G06/wanBlockSwap.md) | 1 |

## E01 SDXL SD3 与 Refiner 条件

| 节点 | 用例数 |
|---|---|
| [CLIPTextEncodeSD3](E01/CLIPTextEncodeSD3.md) | 2 |
| [CLIPTextEncodeSDXLRefiner](E01/CLIPTextEncodeSDXLRefiner.md) | 3 |
| [CLIPTextEncodeSDXL](E01/CLIPTextEncodeSDXL.md) | 3 |
| [EmptySD3LatentImage](E01/EmptySD3LatentImage.md) | 4 |

## E02 Flux 与多参考

| 节点 | 用例数 |
|---|---|
| [CLIPTextEncodeFlux](E02/CLIPTextEncodeFlux.md) | 3 |
| [FluxKontextMultiReferenceLatentMethod](E02/FluxKontextMultiReferenceLatentMethod.md) | 2 |
| [FluxDisableGuidance](E02/FluxDisableGuidance.md) | 2 |
| [FluxGuidance](E02/FluxGuidance.md) | 3 |
| [FluxKontextImageScale](E02/FluxKontextImageScale.md) | 1 |
| [EmptyFlux2LatentImage](E02/EmptyFlux2LatentImage.md) | 4 |
| [USOStyleReference](E02/USOStyleReference.md) | 2 |
| [Flux2Scheduler](E02/Flux2Scheduler.md) | 4 |

## E03 Qwen 图像编辑与分层

| 节点 | 用例数 |
|---|---|
| [TextEncodeQwenImageEdit](E03/TextEncodeQwenImageEdit.md) | 3 |
| [TextEncodeQwenImageEditPlus](E03/TextEncodeQwenImageEditPlus.md) | 3 |
| [EmptyQwenImageLayeredLatentImage](E03/EmptyQwenImageLayeredLatentImage.md) | 4 |
| [QwenImageDiffsynthControlnet](E03/QwenImageDiffsynthControlnet.md) | 3 |

## E04 HiDream 图像与参考条件

| 节点 | 用例数 |
|---|---|
| [CLIPTextEncodeHiDream](E04/CLIPTextEncodeHiDream.md) | 2 |
| [HiDreamO1ReferenceImages](E04/HiDreamO1ReferenceImages.md) | 2 |
| [EmptyHiDreamO1LatentImage](E04/EmptyHiDreamO1LatentImage.md) | 4 |

## E05 其他图像家族的编码与编辑

| 节点 | 用例数 |
|---|---|
| [TextEncodeBooguEdit](E05/TextEncodeBooguEdit.md) | 3 |
| [CLIPTextEncodeHunyuanDiT](E05/CLIPTextEncodeHunyuanDiT.md) | 2 |
| [TextEncodeJoyImageEdit](E05/TextEncodeJoyImageEdit.md) | 3 |
| [CLIPTextEncodeLumina2](E05/CLIPTextEncodeLumina2.md) | 2 |
| [TextEncodeMageFlowEdit](E05/TextEncodeMageFlowEdit.md) | 4 |
| [CLIPTextEncodePixArtAlpha](E05/CLIPTextEncodePixArtAlpha.md) | 3 |
| [TextEncodeZImageOmni](E05/TextEncodeZImageOmni.md) | 3 |
| [EmptyChromaRadianceLatentImage](E05/EmptyChromaRadianceLatentImage.md) | 4 |
| [EmptyHunyuanImageLatent](E05/EmptyHunyuanImageLatent.md) | 4 |
| [ZImageFunControlnet](E05/ZImageFunControlnet.md) | 3 |

## E06 多阶段生成与专项图像处理

| 节点 | 用例数 |
|---|---|
| [DifferentialDiffusion](E06/DifferentialDiffusion.md) | 3 |
| [StableCascade_SuperResolutionControlnet](E06/StableCascade_SuperResolutionControlnet.md) | 2 |
| [PiDConditioning](E06/PiDConditioning.md) | 2 |
| [InstructPixToPixConditioning](E06/InstructPixToPixConditioning.md) | 2 |
| [LotusConditioning](E06/LotusConditioning.md) | 2 |
| [StableCascade_StageB_Conditioning](E06/StableCascade_StageB_Conditioning.md) | 2 |
| [SD_4XUpscale_Conditioning](E06/SD_4XUpscale_Conditioning.md) | 3 |
| [StableCascade_EmptyLatentImage](E06/StableCascade_EmptyLatentImage.md) | 3 |
| [StableCascade_StageC_VAEEncode](E06/StableCascade_StageC_VAEEncode.md) | 2 |

## E07 LTX 视频与音频联合潜空间

| 节点 | 用例数 |
|---|---|
| [LTXVDurationPredictor](E07/LTXVDurationPredictor.md) | 2 |
| [GetICLoRAParameters](E07/GetICLoRAParameters.md) | 1 |
| [LTXVReferenceAudio](E07/LTXVReferenceAudio.md) | 2 |
| [LTXVAddGuide](E07/LTXVAddGuide.md) | 2 |
| [LTXVConditioning](E07/LTXVConditioning.md) | 1 |
| [LTXVCropGuides](E07/LTXVCropGuides.md) | 2 |
| [LTXVImgToVideo](E07/LTXVImgToVideo.md) | 6 |
| [LTXVImgToVideoInplace](E07/LTXVImgToVideoInplace.md) | 2 |
| [LTXVConcatAVLatent](E07/LTXVConcatAVLatent.md) | 2 |
| [EmptyLTXVLatentVideo](E07/EmptyLTXVLatentVideo.md) | 5 |
| [LTXVAudioVAEDecode](E07/LTXVAudioVAEDecode.md) | 2 |
| [LTXVAudioVAEEncode](E07/LTXVAudioVAEEncode.md) | 2 |
| [LTXVEmptyLatentAudio](E07/LTXVEmptyLatentAudio.md) | 2 |
| [LTXVLatentUpsampler](E07/LTXVLatentUpsampler.md) | 2 |
| [LTXVSeparateAVLatent](E07/LTXVSeparateAVLatent.md) | 2 |
| [LTXAVTextEncoderLoader](E07/LTXAVTextEncoderLoader.md) | 3 |
| [LTXVAudioVAELoader](E07/LTXVAudioVAELoader.md) | 2 |
| [LTXVScheduler](E07/LTXVScheduler.md) | 3 |
| [LTXVPreprocess](E07/LTXVPreprocess.md) | 1 |

## E08 Hunyuan 视频与超分阶段

| 节点 | 用例数 |
|---|---|
| [HunyuanRefinerLatent](E08/HunyuanRefinerLatent.md) | 3 |
| [HunyuanVideo15SuperResolution](E08/HunyuanVideo15SuperResolution.md) | 3 |
| [HunyuanImageToVideo](E08/HunyuanImageToVideo.md) | 4 |
| [HunyuanVideo15ImageToVideo](E08/HunyuanVideo15ImageToVideo.md) | 4 |
| [TextEncodeHunyuanVideo_ImageToVideo](E08/TextEncodeHunyuanVideo_ImageToVideo.md) | 2 |
| [HunyuanVideo15LatentUpscaleWithModel](E08/HunyuanVideo15LatentUpscaleWithModel.md) | 3 |
| [EmptyHunyuanLatentVideo](E08/EmptyHunyuanLatentVideo.md) | 5 |
| [EmptyHunyuanVideo15Latent](E08/EmptyHunyuanVideo15Latent.md) | 5 |

## E09 Cosmos Kandinsky Mochi 与 SVD 视频

| 节点 | 用例数 |
|---|---|
| [NormalizeVideoLatentStart](E09/NormalizeVideoLatentStart.md) | 2 |
| [CosmosImageToVideoLatent](E09/CosmosImageToVideoLatent.md) | 4 |
| [CosmosPredict2ImageToVideoLatent](E09/CosmosPredict2ImageToVideoLatent.md) | 4 |
| [CLIPTextEncodeKandinsky5](E09/CLIPTextEncodeKandinsky5.md) | 2 |
| [Kandinsky5ImageToVideo](E09/Kandinsky5ImageToVideo.md) | 4 |
| [SVD_img2vid_Conditioning](E09/SVD_img2vid_Conditioning.md) | 3 |
| [EmptyCosmosLatentVideo](E09/EmptyCosmosLatentVideo.md) | 5 |
| [EmptyMochiLatentVideo](E09/EmptyMochiLatentVideo.md) | 5 |

## E10 自回归视频采样

| 节点 | 用例数 |
|---|---|
| [ARVideoI2V](E10/ARVideoI2V.md) | 4 |
| [EmptyARVideoLatent](E10/EmptyARVideoLatent.md) | 5 |
| [SamplerARVideo](E10/SamplerARVideo.md) | 2 |

## E11 Wan 基础与首末帧

| 节点 | 用例数 |
|---|---|
| [Wan22ImageToVideoLatent](E11/Wan22ImageToVideoLatent.md) | 4 |
| [WanFirstLastFrameToVideo](E11/WanFirstLastFrameToVideo.md) | 4 |
| [WanImageToVideo](E11/WanImageToVideo.md) | 4 |

## E12 Wan 轨迹与相机控制

| 节点 | 用例数 |
|---|---|
| [WanCameraEmbedding](E12/WanCameraEmbedding.md) | 2 |
| [WanCameraImageToVideo](E12/WanCameraImageToVideo.md) | 4 |
| [GenerateTracks](E12/GenerateTracks.md) | 2 |
| [WanMoveConcatTrack](E12/WanMoveConcatTrack.md) | 2 |
| [WanMoveTracksFromCoords](E12/WanMoveTracksFromCoords.md) | 2 |
| [WanMoveTrackToVideo](E12/WanMoveTrackToVideo.md) | 6 |
| [WanMoveVisualizeTracks](E12/WanMoveVisualizeTracks.md) | 2 |
| [WanTrackToVideo](E12/WanTrackToVideo.md) | 4 |

## E13 Wan 遮罩 控制与主体参考

| 节点 | 用例数 |
|---|---|
| [Wan22FunControlToVideo](E13/Wan22FunControlToVideo.md) | 4 |
| [WanFunControlToVideo](E13/WanFunControlToVideo.md) | 4 |
| [WanFunInpaintToVideo](E13/WanFunInpaintToVideo.md) | 4 |
| [WanPhantomSubjectToVideo](E13/WanPhantomSubjectToVideo.md) | 4 |
| [WanVaceToVideo](E13/WanVaceToVideo.md) | 6 |
| [WanUni3CControlnetApply](E13/WanUni3CControlnetApply.md) | 5 |

## E14 Wan 人体动作与 SCAIL

| 节点 | 用例数 |
|---|---|
| [WanAnimate2Cache](E14/WanAnimate2Cache.md) | 2 |
| [WanAnimate2ToVideo](E14/WanAnimate2ToVideo.md) | 5 |
| [WanAnimateToVideo](E14/WanAnimateToVideo.md) | 4 |
| [SCAIL2ColoredMask](E14/SCAIL2ColoredMask.md) | 2 |
| [WanSCAILToVideo](E14/WanSCAILToVideo.md) | 5 |

## E15 Wan 音频驱动与续接

| 节点 | 用例数 |
|---|---|
| [WanDancerPadKeyframes](E15/WanDancerPadKeyframes.md) | 2 |
| [WanDancerPadKeyframesList](E15/WanDancerPadKeyframesList.md) | 2 |
| [AudioEncoderEncode](E15/AudioEncoderEncode.md) | 2 |
| [WanDancerEncodeAudio](E15/WanDancerEncodeAudio.md) | 2 |
| [WanDancerVideo](E15/WanDancerVideo.md) | 4 |
| [WanHuMoImageToVideo](E15/WanHuMoImageToVideo.md) | 4 |
| [WanInfiniteTalkToVideo](E15/WanInfiniteTalkToVideo.md) | 4 |
| [WanSoundImageToVideo](E15/WanSoundImageToVideo.md) | 4 |
| [WanSoundImageToVideoExtend](E15/WanSoundImageToVideoExtend.md) | 3 |
| [AudioEncoderLoader](E15/AudioEncoderLoader.md) | 2 |

## E16 VOID 视频修补与光流噪声

| 节点 | 用例数 |
|---|---|
| [VOIDQuadmaskPreprocess](E16/VOIDQuadmaskPreprocess.md) | 1 |
| [VOIDInpaintConditioning](E16/VOIDInpaintConditioning.md) | 4 |
| [VOIDWarpedNoise](E16/VOIDWarpedNoise.md) | 4 |
| [VOIDWarpedNoiseSource](E16/VOIDWarpedNoiseSource.md) | 2 |
| [OpticalFlowLoader](E16/OpticalFlowLoader.md) | 2 |
| [VOIDSampler](E16/VOIDSampler.md) | 2 |

## E17 Hunyuan 三维生成与体素网格

| 节点 | 用例数 |
|---|---|
| [VoxelToMesh](E17/VoxelToMesh.md) | 2 |
| [VoxelToMeshBasic](E17/VoxelToMeshBasic.md) | 2 |
| [Hunyuan3Dv2Conditioning](E17/Hunyuan3Dv2Conditioning.md) | 2 |
| [Hunyuan3Dv2ConditioningMultiView](E17/Hunyuan3Dv2ConditioningMultiView.md) | 2 |
| [EmptyLatentHunyuan3Dv2](E17/EmptyLatentHunyuan3Dv2.md) | 3 |
| [VAEDecodeHunyuan3D](E17/VAEDecodeHunyuan3D.md) | 2 |

## E18 Trellis 与其它三维阶段条件

| 节点 | 用例数 |
|---|---|
| [BerniniConditioning](E18/BerniniConditioning.md) | 4 |
| [Pixal3DConditioning](E18/Pixal3DConditioning.md) | 2 |
| [Trellis2UpsampleStage](E18/Trellis2UpsampleStage.md) | 2 |
| [Trellis2Conditioning](E18/Trellis2Conditioning.md) | 2 |
| [Trellis2ShapeStage](E18/Trellis2ShapeStage.md) | 2 |
| [Trellis2TextureStage](E18/Trellis2TextureStage.md) | 2 |
| [EmptyTrellis2LatentStructure](E18/EmptyTrellis2LatentStructure.md) | 3 |
| [VaeDecodeShapeTrellis](E18/VaeDecodeShapeTrellis.md) | 2 |
| [VaeDecodeStructureTrellis2](E18/VaeDecodeStructureTrellis2.md) | 2 |
| [VaeDecodeTextureTrellis](E18/VaeDecodeTextureTrellis.md) | 2 |

## E19 TripoSplat 生成

| 节点 | 用例数 |
|---|---|
| [TripoSplatConditioning](E19/TripoSplatConditioning.md) | 2 |
| [TripoSplatPreprocessImage](E19/TripoSplatPreprocessImage.md) | 2 |
| [VAEDecodeTripoSplat](E19/VAEDecodeTripoSplat.md) | 3 |
| [TripoSplatSamplingPreview](E19/TripoSplatSamplingPreview.md) | 2 |

## E20 多视角图像与相机条件

| 节点 | 用例数 |
|---|---|
| [SV3D_Conditioning](E20/SV3D_Conditioning.md) | 2 |
| [StableZero123_Conditioning](E20/StableZero123_Conditioning.md) | 2 |
| [StableZero123_Conditioning_Batched](E20/StableZero123_Conditioning_Batched.md) | 2 |

## E21 音频 VAE 与音频生成家族

| 节点 | 用例数 |
|---|---|
| [ReferenceTimbreAudio](E21/ReferenceTimbreAudio.md) | 2 |
| [TextEncodeAceStepAudio](E21/TextEncodeAceStepAudio.md) | 2 |
| [TextEncodeAceStepAudio1.5](E21/TextEncodeAceStepAudio1.5.md) | 3 |
| [MiniMaxMusic3TextEncode](E21/MiniMaxMusic3TextEncode.md) | 3 |
| [ConditioningStableAudio](E21/ConditioningStableAudio.md) | 1 |
| [EmptyLatentAudio](E21/EmptyLatentAudio.md) | 4 |
| [VAEEncodeAudio](E21/VAEEncodeAudio.md) | 2 |
| [EmptyAceStepLatentAudio](E21/EmptyAceStepLatentAudio.md) | 4 |
| [EmptyAceStep1.5LatentAudio](E21/EmptyAceStep1.5LatentAudio.md) | 4 |
| [EmptyMiniMaxMusic3LatentAudio](E21/EmptyMiniMaxMusic3LatentAudio.md) | 4 |

## E22 SeedVR2 与 SUPIR 修复

| 节点 | 用例数 |
|---|---|
| [SeedVR2PostProcessing](E22/SeedVR2PostProcessing.md) | 2 |
| [SeedVR2Preprocess](E22/SeedVR2Preprocess.md) | 2 |
| [SeedVR2Conditioning](E22/SeedVR2Conditioning.md) | 2 |
| [SeedVR2TemporalMerge](E22/SeedVR2TemporalMerge.md) | 2 |
| [SeedVR2TemporalChunk](E22/SeedVR2TemporalChunk.md) | 2 |
| [SUPIRApply](E22/SUPIRApply.md) | 2 |

## E23 语言生成与专用提示词

| 节点 | 用例数 |
|---|---|
| [Ideogram4Scheduler](E23/Ideogram4Scheduler.md) | 4 |
| [TextGenerateLTX2Prompt](E23/TextGenerateLTX2Prompt.md) | 2 |
| [TextGenerate](E23/TextGenerate.md) | 2 |

## E24 扩展模型补丁加载

| 节点 | 用例数 |
|---|---|
| [HypernetworkLoader](E24/HypernetworkLoader.md) | 3 |
| [ModelPatchLoader](E24/ModelPatchLoader.md) | 2 |
| [AnimaLLLiteApply](E24/AnimaLLLiteApply.md) | 5 |
