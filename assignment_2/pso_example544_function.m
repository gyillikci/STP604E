function f=pso_example544_function(x)  

n0 = x(1);
n30 = x(2);
n45 = x(3);
n60 = x(4);
n90 = x(5);

Nx = 10000;
Nxy = 3000;
epsx_lim = 0.004;
gammaxy_lim = 0.006;

A11 = 0.186717*n0 + 0.230683*n30 + 0.127219*n45 + 0.230683*n60 + 0.0190754*n90;
A22 = 0.0190754*n0+0.0630414*n30+0.127219*n45+0.0630414*n60+0.186717*n90;
A12 = 0.00572262*n0+0.0703753*n30+0.0900187*n45+0.0703753*n60+0.00572262*n90;
A66 = 0.0093*n0+0.0775301*n30+0.0971735*n45+0.0775301*n60+0.0093*n90;

A = [A11 A12 0; A12 A22 0; 0 0 A66]*10^6;

N = [Nx; 0; Nxy];

eps = inv(A)*N;


of = 2*(n0+n90)+4*(n30+n45+n60);

c0(1) = eps(1)-epsx_lim;
c0(2) = eps(3)-gammaxy_lim;
% c0(3) = 1-n0-n30-n45-n60-n90;

% defining penalty for each constraint 
for i=1:length(c0)     
    if c0(i)>0 || c0(i) == Inf || c0(i) == -Inf        
        c(i)=1;
    else
        c(i)=0;     
    end
end
penalty=1000000;         % penalty on each constraint violation 
f=of+penalty*sum(c);     % fitness function
