import omni.ui as ui
from omni.ui import scene as sc
from .useful_functions import Func

import carb

class LegendOverlay:
    #---------------------------------------#
    # Functions to create Legend Paramaters #
    #---------------------------------------#
    # Make Legend parameter
    def makeLegendParam(selected_prims, legendColors, dataToFind):
        # Create a list of all data in the custom attribute dataToFind in selected prims
        dataList = LegendOverlay.findData(selected_prims, dataToFind)
        # Find min and max of that dataList
        min = dataList[0]
        max = dataList[0]
        legendParam = {}
        for data in dataList:
            if data<min: 
                min = data
            if data>max:
                max = data 
        # Create legend paramater, main use to determine color of mesh 
        legendParam.update({"min" : min})
        legendParam.update({"max" : max})
        legendParam.update({"steps" : len(legendColors)})
        legendParam.update({"step size" : (max+1-min)/len(legendColors)})

        return legendParam 
    
    # Main method to create list of all data in selected rpims
    def findData(selected_prims, dataToFind):
        tmp = []
        for s in selected_prims:
            curr_prim = Func.getPrimAtPath(s)
            # determine if s is a mesh or layer
            if len(curr_prim.GetChildren()) == 0:
                tmp += [curr_prim.GetAttribute(dataToFind).Get()]
            else:
                tmp += LegendOverlay.findLayerData(curr_prim.GetChildren(), dataToFind)
        return tmp
    
    def findLayerData(children, dataToFind):
        if len(children)==0:
            return []
        # determine if children[0] is a mesh or a layer
        if len(children[0].GetChildren())==0:
            return [children[0].GetAttribute(dataToFind).Get()] + LegendOverlay.findLayerData(children[1:], dataToFind)
        return LegendOverlay.findLayerData(children[0].GetChildren(), dataToFind) + LegendOverlay.findLayerData(children[1:], dataToFind)

    #----------------------------------#
    # Functions to make legend overlay #
    #----------------------------------#
    # Make a Legend that overlays on top of the viewport
    def make_legend_overlay(direction, legendColors, viewport_window):
        if viewport_window is not None:
            # Clear anything already overlayed on viewport, then get the positions and size of each legend piece
            viewport_window.frame.clear()
            trans, scale = LegendOverlay.make_overlay_points(direction, viewport_window, legendColors)
            # Render to viewport frame
            with viewport_window.frame:
                # Set scene view height and width as viewport height and width so that (0,0) will be at the center
                h=viewport_window.height
                w=viewport_window.width
                scene_view = sc.SceneView(
                    aspect_ratio_policy=sc.AspectRatioPolicy.PRESERVE_ASPECT_FIT,
                    height=h,
                    width=w)
                
                # Need scene_view.scene to render ui.scene elements
                with scene_view.scene:
                    # Draw the legend pieces
                    for i in range(len(legendColors)):
                        legColor = (legendColors[i][0], legendColors[i][1], legendColors[i][2], 1)
                        # Couldn't find if Rectangle has property to specify position, so use this translation method to move rectangle
                        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(trans[i][0], trans[i][1], trans[i][2])):
                            sc.Rectangle(color=legColor, height=scale[0], width=scale[1])
                    """Code for Testing
                    aspect_ratio = w/h
                    height = 0.945
                    sc.Rectangle(color=(1,1,1,1), height=2, width=2)
                    sc.Line([-1*aspect_ratio+0.01,-1*height,0], [aspect_ratio-0.05, 1, 0], color=(0,0,1,1), thickness=5)
                    sc.Line([-1*aspect_ratio+0.01,1,0], [aspect_ratio-0.05, -1*height, 0], color=(0,0,1,1), thickness=5)

                    sc.Line([0, -1*height, 0], [0, 1, 0], color=(1,0,0,1), thickness=5)
                    sc.Line([-1*aspect_ratio+0.01, 0, 0], [aspect_ratio-0.05, 0, 0], color=(1,0,0,1), thickness=5)
                    print("SJSJSJSJSJSJSJSJS")
                    for i in range(10):
                        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(i, 0, 0)):
                            sc.Rectangle(color=(1,1,1,1), height=1, width=1)
                    with sc.Transform(transform=sc.Matrix44.get_translation_matrix(-1*w/10000*13, 0, 0)):
                        sc.Rectangle(color=cl.white, height=h/10000, width=w/10000)
                    stepsize = 2*w/10000*13/len(legendColors)
                    with sc.Transform(transform=sc.Matrix44.get_translation_matrix(-1*w/10000*13 + 2*stepsize-stepsize/2.0, h/10000*13, 0)):
                        sc.Rectangle(color=cl.white, height=h/10000, width=w/10000)
                    print(-1*w/10000*13 + 2*stepsize-stepsize/2.0)
                    print(trans)"""
             
    # Returns a 2D array trans for the positions of each legend piece, 
    # and returns a 2 element array [height, width] for each legend piece
    def make_overlay_points(direction, viewport_window, legendColors):
        # For doing calculations
        h=viewport_window.height
        w=viewport_window.width
        aspect_ratio = w/h
        legColLen = len(legendColors)
        margin = 0.1 #percentage offset from edges
        # Dict for the min, max values of the viewport frame, calculated with magic numbers
        coordSys = {"-x": -1*aspect_ratio+0.01, 
                    "+x": aspect_ratio-0.05, 
                    "-y": -0.945, 
                    "+y": 1}
        # return variables
        trans = []
        scale = []
        # Numbers for if legend will be on top or bottom
            #percent of total viewport height the legend will take up
            #the height of each legend piece that will also be the offset from the border
            #how wide each legend piece is, accounting for margins
        percH = 0.05
        offsetAndHeight = percH*(coordSys["+y"]-coordSys["-y"])
        stepSizeHoriz = (1-2*margin)*(coordSys["+x"]-coordSys["-x"])/legColLen
        # Numbers for if legend will be on left or rightns
        percW = 0.02
        offsetAndWidth = percW*(coordSys["+x"]-coordSys["-x"])
        stepSizeVert = (1-2*margin)*(coordSys["+y"]-coordSys["-y"])/legColLen
        # Calc trans and scale 
        if(direction=='top'):
            for i in range(legColLen):
                trans.append([coordSys["-x"] + (margin)*(coordSys["+x"]-coordSys["-x"]) + stepSizeHoriz*(i+1) - stepSizeHoriz/2.0, 
                            coordSys["+y"] - offsetAndHeight, 
                            0])
            scale = [offsetAndHeight, stepSizeHoriz]
        elif(direction=='bottom'):
            for i in range(legColLen):
                trans.append([coordSys["-x"] + (margin)*(coordSys["+x"]-coordSys["-x"]) + stepSizeHoriz*(i+1) - stepSizeHoriz/2.0, 
                            coordSys["-y"] + offsetAndHeight , 
                            0])
            scale = [offsetAndHeight, stepSizeHoriz]
        elif(direction=='left'):
            for i in range(legColLen):
                trans.append([coordSys["-x"] + offsetAndWidth, 
                            coordSys["-y"] + (margin)*(coordSys["+y"]-coordSys["-y"])+ stepSizeVert*(i+1)- stepSizeVert/2.0, 
                            0])
            scale = [stepSizeVert, offsetAndWidth]
        elif(direction=='right'):
            for i in range(legColLen):
                trans.append([coordSys["+x"] - offsetAndWidth, 
                            coordSys["-y"] + (margin)*(coordSys["+y"]-coordSys["-y"]) + stepSizeVert*(i+1)- stepSizeVert/2.0, 
                            0])
            scale = [stepSizeVert, offsetAndWidth]
        return trans, scale