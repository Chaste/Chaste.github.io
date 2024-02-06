---
title: "Useful Notes for Debugging Parallel Code"
description: "Useful Notes for Debugging Parallel Code"
draft: false
images: []
toc: true
layout: "single"
---

## GDB in parallel

Adding the following to `~/.bashrc` enables you to launch gdb in parallel with each process having its own terminal window. The `-ex run` bit is optional but saves you clicking in each terminal window and typing run.


```

paragdb()
{
    mpirun -np $1 xterm -e gdb -ex run $2
}
alias gdbp=paragdb

```


You may run a compiled test by typing,


```

gdbp 12 cell_based/build/debug/population/TestNodeBasedCellPopulationParallelMethodsRunner

```


where 12 is the number of processes you want to launch.
