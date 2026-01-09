function f=pso_mishrasbird_function(x)  


of = sin(x(2))*exp((1-cos(x(1)))^2)+cos(x(1))*exp((1-sin(x(2)))^2)+(x(1)-x(2))^2;

c0(1) = (x(1)+5)^2+(x(2)+5)^2-25;


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

% f = of;