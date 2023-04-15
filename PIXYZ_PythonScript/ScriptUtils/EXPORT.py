scene.mergeParts([1])
scene.compress()
io.exportScene("E:/Wk_UnrealEngine_Library/Model_opt/Park_QHS.fbx", 0)
core.resetSession()

scenario.generateLODChain([1], [pxz.scenario.DecimateParameters(20.000000, 10.000000, 5.000000), pxz.scenario.DecimateParameters(100.000000, 50.000000, 10.000000), pxz.scenario.DecimateParameters(1000.000000, 100.000000, 20.000000)])
