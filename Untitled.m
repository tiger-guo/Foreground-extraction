source1 = VideoReader('SIFT/campus4-c0.mp4');
source2 = VideoReader('SIFT/campus4-c1.mp4');
source3 = VideoReader('SIFT/terrace1-c0.mp4');
source4 = VideoReader('SIFT/terrace1-c1.mp4');
nFrames1 = source1.NumberOfFrames;
nFrames2 = source2.NumberOfFrames;
nFrames3 = source3.NumberOfFrames;
nFrames4 = source4.NumberOfFrames;
bg1=double(rgb2gray(read(source1,1)));
bg2=double(rgb2gray(read(source2,1)));
bg3=double(rgb2gray(read(source3,1)));
bg4=double(rgb2gray(read(source4,1)));
[m,n]=size(bg1);
theld=40; clors=['b' 'r' 'g' 'k' 'y' 'c' 'm'];
bFirst=1;
bFirst2=1;
bFirst3=1;
bFirst4=1;

for i = 500:1000
    a1 = double(rgb2gray(read(source1,i))); % read in frame
    a2 = double(rgb2gray(read(source2,i)));
    a3 = double(rgb2gray(read(source3,i))); % read in frame
    a4 = double(rgb2gray(read(source4,i)));
    det1=abs(a1-bg1);
    det2=abs(a2-bg2);
    det3=abs(a3-bg3);
    det4=abs(a4-bg4);
    det1(det1<theld)=0;
    det1(det1>=theld)=1;
     se1=strel('diamond', 10);
    det1=imdilate(det1,se1); %图像膨胀
    det1=bwareaopen(det1,1000);%去除图像中面积小�? 500 的区�?
    det2(det2<theld)=0;
    det2(det2>=theld)=1;
    sel2=strel('diamond', 10);
    det2=imdilate(det2,sel2); %图像膨胀
    det2=bwareaopen(det2,1000);
    det3(det3<theld)=0;
    det3(det3>=theld)=1;
    se3=strel('diamond', 10);
    det3=imdilate(det3,se3); %图像膨胀
    det3=bwareaopen(det3,1000);%去除图像中面积小�? 500 的区�?
    det4(det4<theld)=0;
    det4(det4>=theld)=1;
    se4=strel('diamond', 10);
    det4=imdilate(det4,se4); %图像膨胀
    det4=bwareaopen(det4,1000);%去除图像中面积小�? 500 的区�?
    % % % det2= imfill(det2,'holes');%将原图填充孔�?
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% �? �? 分割%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    box1=regionprops(det1,'BoundingBox');
    box2=regionprops(det2,'BoundingBox');
    box3=regionprops(det3,'BoundingBox');
    box4=regionprops(det4,'BoundingBox');


    for i=1:length(box1)
        box1(i).BoundingBox=round(box1(i).BoundingBox);
        if box1(i).BoundingBox(1)+box1(i).BoundingBox(3)>n
            box1(i).BoundingBox(3)=n-box1(i).BoundingBox(1);
        end
        if box1(i).BoundingBox(2)+box1(i).BoundingBox(4)>m
            box1(i).BoundingBox(4)=m-box1(i).BoundingBox(2);
        end
    end
    for i=1:length(box2)
        box2(i).BoundingBox=round(box2(i).BoundingBox);
        if box2(i).BoundingBox(1)+box2(i).BoundingBox(3)>n
            box2(i).BoundingBox(3)=n-box2(i).BoundingBox(1);
        end
        if box2(i).BoundingBox(2)+box2(i).BoundingBox(4)>m
            box2(i).BoundingBox(4)=m-box2(i).BoundingBox(2);
        end
    end
    for i=1:length(box3)
        box3(i).BoundingBox=round(box3(i).BoundingBox);
        if box3(i).BoundingBox(1)+box3(i).BoundingBox(3)>n
            box3(i).BoundingBox(3)=n-box3(i).BoundingBox(1); end
        if box3(i).BoundingBox(2)+box3(i).BoundingBox(4)>m
            box3(i).BoundingBox(4)=m-box3(i).BoundingBox(2); end
    end
    for i=1:length(box4)
        box4(i).BoundingBox=round(box4(i).BoundingBox);
        if box4(i).BoundingBox(1)+box4(i).BoundingBox(3)>n
            box4(i).BoundingBox(3)=n-box4(i).BoundingBox(1);
        end
        if box4(i).BoundingBox(2)+box4(i).BoundingBox(4)>m
            box4(i).BoundingBox(4)=m-box4(i).BoundingBox(2);
        end
    end
    if length(box1)>0
        if bFirst==1
            boxOld1=box1;
            bFirst=0;
        else
            [boxOld1,num] = RectAna(boxOld1, box1,det1,m,n);
        end
    else
        boxOld1=box1;
    end
    if length(box2)>0
        if bFirst2==1
            boxOld2=box2;
            bFirst2=0;
        else
            [boxOld2,num] = RectAna(boxOld2, box2,det2,m,n);
        end
    else
        boxOld2=box2;
    end
    if length(box3)>0
        if bFirst3==1
            boxOld3=box3;
            bFirst3=0;
        else
            [boxOld3,num] = RectAna(boxOld3, box3,det3,m,n);
        end
    else
        boxOld3=box3;
    end
    if length(box4)>0
        if bFirst4==1
            boxOld4=box4;
            bFirst4=0;
        else
            [boxOld4,num] = RectAna(boxOld4, box4,det4,m,n);
        end
    else
            boxOld4=box4;
    end
    
    figure1 = figure(1); 
    subplot(221),imshow(det1); 
    subplot(222),imshow(det2); 
    subplot(223),imshow(det3); 
    subplot(224),imshow(det4);
    
    figure2 = figure(2);
    subplot(221),imshow(uint8(a1));
    hold on
    for j=1:length(boxOld1)
        rectangle('position',boxOld1(j).BoundingBox,'edgecolor',clors(j));
        text(boxOld1(j).BoundingBox(1)+boxOld1(j).BoundingBox(3)/2-10,boxOld1(j).BoundingBox(2)+boxOld1(j).BoundingBox(4)/2,num2str(j),'FontSize',16,'FontWeight','Bold','Color',clors(j));
    end
    hold off
    subplot(222),imshow(uint8(a2));
    hold on
    for j=1:length(boxOld2)
        rectangle('position',boxOld2(j).BoundingBox,'edgecolor',clors(j));
        text(boxOld2(j).BoundingBox(1)+boxOld2(j).BoundingBox(3)/2-10,boxOld2(j).BoundingBox(2)+boxOld2(j).BoundingBox(4)/2,num2str(j),'FontSize',16,'FontWeight','Bold','Color',clors(j));
    end
    hold off
    subplot(223),imshow(uint8(a3));
    hold on
    for j=1:length(boxOld3)
        rectangle('position',boxOld3(j).BoundingBox,'edgecolor',clors(j));
        text(boxOld3(j).BoundingBox(1)+boxOld3(j).BoundingBox(3)/2-10,boxOld3(j).BoundingBox(2)+boxOld3(j).BoundingBox(4)/2,num2str(j),'FontSize',16,'FontWeight','Bold','Color',clors(j));
    end
    hold off
    subplot(224),imshow(uint8(a4));
    hold on
    for j=1:length(boxOld4)
        rectangle('position',boxOld4(j).BoundingBox,'edgecolor',clors(j));
        text(boxOld4(j).BoundingBox(1)+boxOld4(j).BoundingBox(3)/2-10,boxOld4(j).BoundingBox(2)+boxOld4(j).BoundingBox(4)/2,num2str(j),'FontSize',16,'FontWeight','Bold','Color',clors(j));
    end
    hold off

end
clear;