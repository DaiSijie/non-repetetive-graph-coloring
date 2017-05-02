
def benchmark():
	
	graphs = list()
	names = list()


	G1 = "version=1:1;a;2;b;3;c;4;d;5;e:a,1;2,1;5,1;c,a;d,a;b,2;3,2;d,b;e,b;c,3;4,3;e,c;d,4;5,4;e,5" #Petersen graph
	G2 = "version=1:1;2;3;4;5;6;7;8;9:2,1;3,1;4,1;7,1;3,2;5,2;8,2;6,3;9,3;5,4;6,4;7,4;6,5;8,5;9,6;8,7;9,7;9,8" #R33
	G3 = "version=1:11;12;13;14;15;0;1;2;3;4;5;6;7;8;9;10:3,11;15,11;7,11;8,11;9,11;13,12;14,12;4,12;15,12;8,12;14,13;15,13;5,13;9,13;2,14;15,14;6,14;3,15;7,15;12,0;1,0;2,0;3,0;4,0;8,0;13,1;2,1;3,1;5,1;9,1;3,2;6,2;7,3;5,4;6,4;7,4;8,4;6,5;7,5;9,5;7,6;9,8;11,10;2,10;14,10;6,10;8,10;9,10" #R44
	G4 = "version=1:a;b;c;d;e;f;g;h;i;j:b,a;c,a;d,a;e,a;f,a;g,a;h,a;i,a;j,a;c,b;d,b;e,b;f,b;g,b;h,b;i,b;j,b;d,c;e,c;f,c;g,c;h,c;i,c;j,c;e,d;f,d;g,d;h,d;i,d;j,d;f,e;g,e;h,e;i,e;j,e;g,f;h,f;i,f;j,f;h,g;i,g;j,g;i,h;j,h;j,i" #K10
	G5 = #put some trees here!
	G6
	G7
	G8
	....

	Gs = list()

	ts = [0] * 8
	ts[0] = time.time()
	for i in xrange(len(Gs)):
		#solve problem
		ts[i] = time.time()

	print "================ RESULTS ================"
	print "Time spent: " + ts[8] - ts[0]
	for i in xrange(len(graphs)):
		print "For " + names[i] + ": " + str(ts[i] - ts[i-1])
	print "========================================="






	t1 = time.time()








if __name__ == "__main__":
	benchmark()


