import fs from 'node:fs/promises';
import { finalizePresentation } from '/Users/bagnesium/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations/container_tools/artifact_tool_utils.mjs';
const root='/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/daryn-defense-20260912';
const skill='/Users/bagnesium/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const result=await finalizePresentation({
 workspaceDir:root,candidatePath:root+'/.build/candidate-v2.pptx',finalPath:root+'/output/Kiodai_Daryn_2026_defense.pptx',
 pythonExecutable:'/Users/bagnesium/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
 integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',
 layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','11','--require-native-table-slide','13'],
 explicitTotalSlideCount:14,requiredNativeChartOwnerSlides:[5,6],requiredNativeTableOwnerSlides:[11,13],materializeLiteralChartWorkbooks:true,
 fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,
 receiptPath:root+'/.build/validation-v3.json'
});
console.log(JSON.stringify(result,null,2));
