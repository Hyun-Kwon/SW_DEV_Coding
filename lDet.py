class LD:
	count = 0
	def grayscale(image):
	        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
 
	def canny(image,low_thd,high_thd):
        	return cv2.Canny(image,low_thd,high_thd,apertureSize=5)
 
	def gaussian_blur(image,kernel_size):
        	return cv2.GaussianBlur(image,(kernel_size,kernel_size),0)
 
	def region_of_interest(image, vertices, color3=(255,255,25), color1 = 255):
	        mask = np.zeros_like(image)
        	if len(image.shape)>2:
        	        color = color3
        	else:
        	        color = color1
        	cv2.fillPoly(mask,vertices,color)
        	ROI_image = cv2.bitwise_and(image,mask)
        	return ROI_image
 
	def draw_fit_line(image, lines, color=[0,0,255], thickness=10):
        	cv2.line(image,(lines[0],lines[1]), (lines[2],lines[3]), color, thickness)
 
	def hough_lines(image,rho,theta,threshold,min_line_len,max_line_gap):
        	lines = cv2.HoughLinesP(image,rho,theta,threshold,np.array([]),minLineLength=min_line_len,maxLineGap = m$
        	return lines
 
	def weighted_img(image,initial_img,a=0.7,b=1.5,r=0.):
	        return cv2.addWeighted(initial_img,a,image,b,r)
 
	def get_fitline(image,f_lines):
	        lines = np.squeeze(f_lines)
	        lines = lines.reshape(lines.shape[0]*2,2)
	        rows,cols = image.shape[:2]
	        output = cv2.fitLine(lines,cv2.DIST_L2,0,0.01,0.01)
	        vx,vy,x,y = output[0],output[1],output[2],output[3]
	        slope = output[1]/output[0]
	        intercept=output[3]-(slope*output[2])   
	        x1,y1 = int(((image.shape[0]-1)-intercept)/slope),image.shape[0]-1
	        x2,y2 = int(((image.shape[0]-539)-intercept)/slope),image.shape[0]-539
	        result = [x1,y1,x2,y2]
	        return result
 
	def line(p1,p2):
	        A = (p1[1] - p2[1])
	        B = (p2[0] - p1[0])
	        C = (p1[0]*p2[1] - p2[0]*p1[1])
	        return A,B,-C
 
	def intersection(L1,L2):
	        D = L1[0]*L2[1] - L1[1]*L2[0]
	        Dx = L1[2]*L2[1] - L1[1]*L2[2]
	        Dy = L1[0]*L2[2] - L1[2]*L2[0]
        	if D != 0:
                	x = Dx/D
                	y = Dy/D
                	result = [x,y]
                	return result
        	else:
                	return False

	def lineDetection(image):

		height,width = 960,540
	        ROI = image[200:540,:]
	        gray_image = grayscale(ROI)
	        blur = gaussian_blur(gray_image,3)
	        canny_image = canny(blur, 600, 800)
	        line_arr = hough_lines(canny_image, 1, 1*np.pi/180,30,10,20)
	        line_arr = np.squeeze(line_arr)
	        slope_degree = (np.arctan2(line_arr[:, 1]-line_arr[:, 3],line_arr[:, 0]-line_arr[:, 2])*180)/np.pi
	        line_arr = line_arr[np.abs(slope_degree)<160]
	        slope_degree = slope_degree[np.abs(slope_degree)<160]
	        line_arr = line_arr[np.abs(slope_degree)>95]
	        slope_degree = slope_degree[np.abs(slope_degree)>95]
	        L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
	        temp = np.zeros((image.shape[0], image.shape[1],3), dtype = np.uint8)
	        L_lines, R_lines = L_lines[:,None],R_lines[:,None]
 
	        if L_lines.any(): 
	                if len(L_lines) >= 2 and L_lines[1] != None :
	                        left_fit_line = get_fitline(ROI,L_lines)
	                        draw_fit_line(ROI, left_fit_line)
 
	        if R_lines.any():
	                if len(R_lines) >= 2 and R_lines[1] != None :
	                        right_fit_line = get_fitline(ROI,R_lines)
	                        draw_fit_line(ROI,right_fit_line)
 
	        if count == 0:
	                vp_slope = -1
	                global count=10
 
	        if vp_slope == -1  :    
	                if L_lines.any() and R_lines.any():
				L1 = line([left_fit_line[0],left_fit_line[1]],[left_fit_line[2],left_fit_line[3]])
	                        R1 = line([right_fit_line[0],right_fit_line[1]],[right_fit_line[2],right_fit_line[3]])
	                        vp = intersection(L1,R1)
	                        vp_slope = (np.arctan2(540-vp[1],480-vp[0])*180)/np.pi
	                else : 
	                        vp_slope = np.abs(slope_degree)
	        else :
	                  L1 = line([left_fit_line[0],left_fit_line[1]],[left_fit_line[2],left_fit_line[3]])
	                  R1 = line([right_fit_line[0],right_fit_line[1]],[right_fit_line[2],right_fit_line[3]])
	                  vp = intersection(L1,R1)
	                  vp_slope = (np.arctan2(540-vp[1],480-vp[0])*180)/np.pi
