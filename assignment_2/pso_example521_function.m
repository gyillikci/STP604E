function f=pso_example521_function(x)  

no = x(1);
nf = x(2);
nn = x(3);

of = -(64.88+11.05*no-4.326*nf-6.724*nn);

c0(1) = 6.724*no+4.326*nf-11.05*nn-44.88;
c0(2) = 1.05+1.082*no-2.163*nf+1.082*nn;
c0(3) = 8-no-2*nf-nn;
c0(4) = no+2*nf+nn-8;

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