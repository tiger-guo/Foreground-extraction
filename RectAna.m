function [rects,num] = RectAna(rectOld, rectNew,bw,m,n) 
num1=length(rectOld); 
num2=length(rectNew);
k=1;
for i=1:num2
if rectNew(i).BoundingBox(3)<rectNew(i).BoundingBox(4)*0.85
    rectTemp(k)=rectNew(i);
    k=k+1; 
elseif rectNew(i).BoundingBox(3)>n/2
    rectTemp(k)=rectNew(i);
    k=k+1;
end
end
if k~=1
    rectNew=rectTemp; num2=length(rectNew); 
end

while num2<num1

end
%原目标特征信息
feaOld=zeros(num1,4);
for i=1:num1
feaOld(i,1)=rectOld(i).BoundingBox(3);
feaOld(i,2)=rectOld(i).BoundingBox(4)/3;
feaOld(i,3)=rectOld(i).BoundingBox(1)+rectOld(i).BoundingBox(3)/2;
feaOld(i,4)=rectOld(i).BoundingBox(2)+rectOld(i).BoundingBox(4)/2;
end
%新目标特征信息
feaNew=zeros(num2,4);
for i=1:num2
    feaNew(i,1)=rectNew(i).BoundingBox(3);
    feaNew(i,2)=rectNew(i).BoundingBox(4)/3;
    feaNew(i,3)=rectNew(i).BoundingBox(1)+rectNew(i).BoundingBox(3)/2;
    feaNew(i,4)=rectNew(i).BoundingBox(2)+rectNew(i).BoundingBox(4)/2; 
end
if num2==num1
    rects=rectOld;
for i=1:num1
    [~,ind] =min(sum((repmat(feaOld(i,:),num1,1)-feaNew).^2,2)); rects(i)=rectNew(ind);
    feaNew(ind,:)=feaNew(ind,:)*100;
end
    num=num1; 
end
if num2>num1
bAdd=0; 
mask=zeros(1,num2); 
rects=rectOld;
for i=1:num1
[~,ind] =min(sum((repmat(feaOld(i,:),num2,1)-feaNew).^2,2)); rects(i)=rectNew(ind);
feaNew(ind,:)=feaNew(ind,:)*100; mask(ind)=1; 
end
for i=1:num2
if mask(i)==0
if rectNew(i).BoundingBox(1)<=5 || rectNew(i).BoundingBox(1)+rectNew(i).BoundingBox(3)>=n-4 || rectNew(i).BoundingBox(2)<=5 || rectNew(i).BoundingBox(2)+rectNew(i).BoundingBox(4)>=m-4
if bAdd==0
rects(num1+1)=rectNew(i); 
elseif rectNew(i).BoundingBox(3)*rectNew(i).BoundingBox(4)>rects(num1+1).BoundingBox(3)*rects(num1+1).BoundingBox(4)
rects(num1+1)=rectNew(i); 
end
end
bAdd=1; 
end
if length(rects)>=4
break; 
end
end
end
num=length(rects);

end
