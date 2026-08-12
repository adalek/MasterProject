# experiments
Without RAG:
01 \
02 Note: didn't display on the final node\
03 \
04 Failed. Note: didn't dispaly final node, only scatter no copy to points, at third try it has the right nodes but the input order of copy to points is inversed

RAG:
04 \
05 \
06 Failed, vex PI using pi
07 Failed
08 \
09 Failed
06 with procedural_staircase_full.md, local failed, houdini quit, computer shut down

06 with procedural_staircase_full.md, deepseek succeed:
  Baseline: Full Example RAG
  Source: examples/full/procedural_spiral_staircase_full.md
  
  Model: DeepSeek
  Prompt tokens: 8592
  Completion tokens: 9566
  Total tokens: 18158
  Finish reason: stop
  Execution: PASS
  Geometry: PASS