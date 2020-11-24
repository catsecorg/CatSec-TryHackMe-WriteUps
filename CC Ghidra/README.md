# CC: CC: Ghidra

A crash course on the reverse engineering tool Ghidra

## Task 1 Intro 


GHIDRA is a tool created by the NSA that allows the user to analyze binaries. It is well known for it's incredible de compiler which converts the assembly in the binary to C.

The GHIDRA download can be found here.

Note: Assembly and C knowledge are highly recommended

Note: Ghidra requires an semi-new version of java(11+). If you do not have the jre or the jdk, you can install it with sudo apt install openjdk-13-jre openjdk-13-jdk

Read the above!

`No answer needed`

## Task 2 Creating A New Project 


Once you've unzipped the ghidra folder and downloaded java, you should see a file structure similar to this.

Execute the ghidraRun file by running and you will arrive on this screen,after ghidra finishes loading.


On this screen navigate to File->New Project->Non-Shared-Project.

On that screen make a project directory, and a name, and click finish.

Read and follow along with the above instructions.
`No answer needed`


## Task 3 Analyzing a Binary 
After creating a project, you will be greeted with a screen similar to this.

Once you're at this screen, go to File->Import File. From there navigate to where you downloaded the included binary "example1" , and import it. (Note, Ghidra will automatically detect what type on binary the file is (Example x86,x86_64). )

From there double click the binary, and you will be prompted to analyze the binary, click Analyze->Yes, and you will see a screen similar to this appear.

(Note: Ghidra has plenty of customization options for analyzation, but for general use the default one's that are selected provide all necessary features.)

This is the main screen for analyzing binaries, and it allows you to see every part, of the binary.

For practical use, the most interesting part of this screen is the "Symbol Tree". It allows you to view all of the files that were imported to create the binary, and view all user created functions.

For example, given the C code:

#include <stdio.h>

int main(){

printf("hi!");

}

You would be able to see main, and printf in the functions tab of the Symbol Tree.


(Note: for general binary analysis, you won't be interested in functions that start with "_" as those are functions created during compilation)

This is incredibly useful, as it allows you to see the functions that the binary creator made.

In the example1 binary, double click the "main" function and you should be presented with this screen.


You are able to see both the disassembly, and the decompilation, on the same screen!

From here you can click around all of the different functions that a binary has, and view the C code and the assembly.

Read and follow along with the above instructions!
`No answer needed`

## Task 4 It's your turn! 
In the previous task, we went through how to analyze a binary. Therefore to practice that skill, I have provided a binary for you to analyze yourself!

How many user created functions(including main) are there
`2`
What is the first variable set to in the main function?
`10`
What is the first variable set to, in the function "fn1"?
`hello`
If you provide the input "1", when you run the binary, what would the output be.(Note you can just run the binary to find this out, but that would defeat the whole purpose!).
`nice!`

#Task 5 Miscellaneous operations 


While the previous tasks, have shown most of what you need to analyze binaries. There are still some tips and tricks that are useful to know.

Section 1 - Patching Binaries.

Occasionally there will be times when you want to patch(The art of changing assembly instructions) a binary. Ghidra offers support for this. In the example binary, navigate to the main function and double click the "return 0", in the decompilation section. You should see this screen.


Right click the asm instruction, MOV EAX,0x0 and click "Patch Instruction". From there you can change it to whatever you want, in this case let's change "MOV EAX,0x0" to MOV EAX,0x1". The decompilation will also update, and you should see this screen


The instructions you patch have an effect on the decompilation, so it's very useful for checking your work :D.

Section 2: Searching

Ghidra supports going to different portions of memory, when given a memory address. Click Navigation(At the top bar)->Go To and input a memory address.

Example:



Note: Ghidra supports plenty of misc operations; however, these are the ones I have used the most.

For a full list see this link.

Read and follow along with above!
`No answer needed`

## Task 6 Final Exam 
You should now be able to competently analyze a binary. Now is the chance to show your skills with this crackme! The final exam is the binary called final_exam.

What outputs the good job message?    
`No answer needed`