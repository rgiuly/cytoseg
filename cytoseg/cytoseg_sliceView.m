function sliceView(img, title)

xLim = [1,size(img,2)];
yLim = [1,size(img,1)];

if nargin == 1
    titleText = inputname(1);
elseif nargin == 2
    titleText = title;
else
    error('wrong number of arguments given to sliceView function');
end

hF = figure('name',sprintf('SliceView: %s',titleText),'Units','Normalized','Position',[0.0109    0.1742    0.5312    0.7692],'NumberTitle','off','toolbar','figure');


hA = axes('Units','Normalized','Xlim',xLim,'Ylim',yLim,'Drawmode','fast');
imgMin = min(img(:));
imgMax = max(img(:));
if imgMin == imgMax
    warning('every pixel in this volume is equal to %f', imgMin)
end
imagesc(img(:,:,1),[imgMin,imgMax]), axis image; xlabel(['slice 1/',num2str(size(img,3))]);
set(hA,'xticklabel',[],'yticklabel',[]);
axPos = get(hA,'Position');
sldStep = 1/(size(img,3)-1);
hSlider = uicontrol(hF,'Style','slider','Units','Normalized',...
    'Position',[axPos(1),axPos(2)-.09,axPos(3),.02],'Value',1,'Min',1,'Max',size(img,3),...
    'Tag','sliceViewSlider','SliderStep',[sldStep,sldStep],'Callback',{@hSlider_Callback});
set(hSlider,'units','normalized');

    function hSlider_Callback(varargin)
        Xlim = get(gca,'xlim'); Ylim = get(gca,'ylim');
        imagesc(img(:,:,round(get(hSlider,'Value'))),[imgMin,imgMax]); axis image;xlabel(['slice ',num2str(round(get(hSlider,'Value'))),'/',num2str(size(img,3))]);
        set(hA,'xticklabel',[],'yticklabel',[],'xlim',Xlim,'Ylim',Ylim);
    end
end
