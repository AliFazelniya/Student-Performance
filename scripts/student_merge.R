raw_dir <- file.path("data", "raw")
mat_path <- file.path(raw_dir, "student-mat.csv")
por_path <- file.path(raw_dir, "student-por.csv")

d1=read.table(mat_path,sep=";",header=TRUE)
d2=read.table(por_path,sep=";",header=TRUE)

d3=merge(d1,d2,by=c("school","sex","age","address","famsize","Pstatus","Medu","Fedu","Mjob","Fjob","reason","nursery","internet"))
print(nrow(d3)) # 382 students
