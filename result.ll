; ModuleID = 'main.ll'
target datalayout = "e-p:64:64:64-S128-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f16:16:16-f32:32:32-f64:64:64-f128:128:128-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64"
target triple = "x86_64-pc-linux-gnu"

@printd = global [2 x i8] c"%d"
@a = global i32 0
@b = global i32 1
@c = global i32 2
@d = global i32 4

define void @main() {
entry:
  %a = load i32* @a
  %b = load i32* @b
  %temp0 = add i32 %a, %b
  %c = load i32* @c
  %d = load i32* @d
  %temp01 = add i32 %c, %d
  %temp02 = add i32 %temp0, %temp01
  store i32 %temp02, i32* @a
  %0 = load i32* @a
  %calltmp = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([2 x i8]* @printd, i32 0, i32 0), i32 %0)
  ret void
  ret void
}

declare i32 @printf(i8*, ...)
