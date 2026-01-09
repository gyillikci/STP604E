tic 
clc 
clear all 
close all 
rng default  

% pso parameters values 
mmm=3;            % number of variables 
nnn=300;          % population size 
wmax=0.9;       % inertia weight 
wmin=0.4;       % inertia weight 
c1=2;           % acceleration factor 
c2=2;           % acceleration factor   

LB = zeros(1,mmm);
UB = 50*ones(1,mmm);


% pso main program 
maxite=100;    % set maximum number of iteration 
maxrun=30;      % set maximum number of runs need to be 
for run=1:maxrun     
    run     
    % pso initialization----------------------------------------------start     

    for iii=1:nnn
        for j=1:mmm
            x0(iii,j)=round(LB(j)+rand()*(UB(j)-LB(j)));
        end
    end
    
    x=x0;       % initial population     
    v=0.1*x0;   % initial velocity     
    for iii=1:nnn   
%         iii
        f0(iii,1)=pso_exercise51_function(x0(iii,:));     
    end
    [fmin0,index0]=min(f0);         
    pbest=x0;               % initial pbest     
    gbest=x0(index0,:);     % initial gbest     
    % pso initialization------------------------------------------------end          

    % pso algorithm---------------------------------------------------start     
    ite=1;         
    tolerance=1;     
    while ite<=maxite && tolerance>10^-12

         w=wmax-(wmax-wmin)*ite/maxite; % update inertial weight           

         % pso velocity updates         
         for iii=1:nnn             
             for j=1:mmm                 
                 v(iii,j)=0.73*(w*v(iii,j)+c1*rand()*(pbest(iii,j)-x(iii,j))...                         
                     +c2*rand()*(gbest(1,j)-x(iii,j)));             
             end
         end

         % pso position update         
         for iii=1:nnn             
             for j=1:mmm                 
                 x(iii,j)=round(x(iii,j)+v(iii,j));             
             end
         end

         % handling boundary violations         
         for iii=1:nnn             
             for j=1:mmm                 
                 if x(iii,j)<LB(j)                     
                     x(iii,j)=LB(j);                 
                 elseif x(iii,j)>UB(j)                     
                     x(iii,j)=UB(j);                 
                 end
             end
         end

         % evaluating fitness         
         for iii=1:nnn
             f(iii,1)=pso_exercise51_function(x(iii,:));
         end

         % updating pbest and fitness         
         for iii=1:nnn             
             if f(iii,1)<f0(iii,1)
                pbest(iii,:)=x(iii,:);                 
                f0(iii,1)=f(iii,1);             
             end
         end
         [fmin,index]=min(f0);   % finding out the best particle         
         ffmin(ite,run)=fmin;    % storing best fitness         
         ffite(run)=ite;         % storing iteration count 

         % updating gbest and best fitness         
         if fmin<fmin0             
             gbest=pbest(index,:);             
             fmin0=fmin;         
         end

         % calculating tolerance         
         if ite>100             
             tolerance=abs(ffmin(ite-100,run)-fmin0);         
         end

         % displaying iterative results         
         if ite==1             
             disp(sprintf('Iteration    Best particle    Objective fun'));         
         end
         disp(sprintf('%8g  %8g          %8.4f',ite,index,fmin0));             
         ite=ite+1;     
    end
    % pso algorithm-----------------------------------------------------end     
    gbest;     
    % fvalue=min(f);
    fvalue=fmin0;
    fff(run)=fvalue;     
    rgbest(run,:)=gbest;     
    disp(sprintf('--------------------------------------'));
end

% pso main program------------------------------------------------------end 
disp(sprintf('\n')); 
disp(sprintf('*********************************************************')); 
disp(sprintf('Final Results-----------------------------')); 
[bestfun,bestrun]=min(fff) 
best_variables=rgbest(bestrun,:) 
disp(sprintf('*********************************************************')); 
toc   

% PSO convergence characteristic 
plot(ffmin(1:ffite(bestrun),bestrun),'-k'); 
xlabel('Iteration'); 
ylabel('Fitness function value'); 
title('PSO convergence characteristic')