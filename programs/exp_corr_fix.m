clear C;
f=1;
for z=1:numel(corr)
if time(z)==30
C(f,1)=corr(z);
f=f+1;
end
end
mean(C)