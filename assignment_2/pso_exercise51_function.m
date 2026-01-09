function f=pso_exercise51_function(x)  

no = x(1);
nf = x(2);
nn = x(3);

of = (no+2*nf+nn);

c0(1) = 0.6-(9.59489*nf+0.471444*nn+0.471444*no)/(11.8949*nf+19.1603*nn+1.3866*no);
c0(2) = -16+(39.208*nf+2.3*nn+2.3*no)/(2*nf+nn+no);
c0(3) = 20-11.8949*nf-19.1603*nn-1.3866*no;


% defining penalty for each constraint 
for i=1:length(c0)     
    if c0(i)>0         
        c(i)=1;     
    else
        c(i)=0;     
    end
end
penalty=1000000;           % penalty on each constraint violation 
f=of+penalty*sum(c);     % fitness function
