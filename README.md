# PIXYZ System Lab

*MyAutomation1 used for Pixyz*
*版本：20230417 实现   PIXYZ 2022.1*

![logo_WK.png](Documentation%2Flogo_WK.png)

# Release Notes & Roadmap
RVT是很标准的，考虑基于此进行开发
在PIXYZ 2021版本之后，导入时默认执行一轮优化策略。一些脚本其实已经没啥用了。未来的目标是基于某一类的模型进行定制化的优化。
另一方面，自从Pixyz被Unity收购之后，各种试用版的限制越来越多，不知道未来会怎么样。所以，这个项目也是为了自己的学习和研究。仅作为一个可行技术路径的探索。
### 3.1 updates

`处理中`


`已解决`
- 实例化ResetTransform时的变形问题
- bug：解决中文字符转拼音的问题
  - 提供了批量化命名的脚本，转化拼音
  - 2023年4月23日 .pxzext更新后，可以识别中文字符了
- 升级：实现多文件夹监控和递归查询文件，梳理IO层级
- UE datasmith 无法识别 fbx 层级结构附带属性的问题。只有SMActor才有AssetUserData。
    - 通过JSON库来导出metadata，进行数模分离






### Situation

1. 多源异构模型数据的聚合。
2. 提升大模型的处理效率和性能。
3. 批量处理服务开发。
4. 针对C端上传模型自动化导入UE5的问题
5. 针对模型处理费力费时，效果差，管控力度不够的问题
6. 针对数据中台的建设需求
7. 针对多源3D模型的IO问题。

### Plan

1. 脚本积累，学习Python。（已完成）
2. 实践应用。基于PixyzStudio设计流程和优化参数。（已完成）
3. 第一阶段：面向RVT的PixyzScript，根据标准构件和层级关系进行项目级优化。（进行中）
4. 第二阶段：面向RVT的PixyzSenerioPlugin。
5. 第三阶段：PixyzScrpt工具库。

- 前提技术基础与难点

- [x]  Python API
- [x]  Pixyz的bug解决
- [x]  AWS部署

## Results




## 2.0 基于 scenario processor 部署后台服务


### Tech Framework
![folder-watcher.png](ByPixyzOfficial%2Fscenario-processor-sample-main%2Fdocumentation%2Ffolder-watcher.png)



`流程：`监控导入文件夹，PIXYZ进行IO和优化，最后提供导出后的文件。98%通过Python实现。
- 只需要区分`文件格式类型`，`输入输出` 就可以黑箱操作导入导出。

### Optimization strategy

1. IO升级，多格式导出。
2. BIM属性识别与Smart挂接。
3. 文件夹监控。
4. json解析，config。
5. 开发流程和配置环境的批处理。
6. RVT模型构件级识别与重组织。
7. 8专业兼容适配，且搭建预设框架，定制化处理类型。
8. 网格Smart合并。
9. 网格Smart点线面坍缩。
10. 文件清理机器人，实时监控，Smart剔除冗余，实例精简。
11. CAD 高级修复，重镶嵌，优化法线，填洞。
12. 质量预设，联动CAD修复和网格优化。
13. 性能提升，查询复杂大模型。
14. 清理无效材质，合并材质，联动处理贴图。
15. 材质ID去重，修复错误ID。
16. 修复LongName溢出。
17. 重置变换，Smart实例化构件。
18. 渲染优化，三角面化，管线优化。
19. 系统优化，调用subprocesss处理。
20. 系统优化，处理粘贴复制的检测冲突。
21. RVT 参考了深圳市的标准文件。基于此进行了测试。


