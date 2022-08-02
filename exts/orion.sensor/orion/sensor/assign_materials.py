import omni.ext
import omni.kit.commands
import omni.usd
from pxr import UsdShade, Sdf
from omni.ui import scene as sc

from .viewport_overlay_legend import LegendOverlay
from .useful_functions import Func

class AssignMat:
    # ------------------------------------------------------------------#
    # Sub-functions to determine color of mesh and create all materials #
    # ------------------------------------------------------------------#
    # Determine color of mesh based on mesh's data attribute
    def determColorIndex(curr_prim, legendParam, dataToRead):
        data = curr_prim.GetAttribute(dataToRead).Get()
        i = 1
        # Determine which step size this data falls under based on the created legend parameters
        while(data>=legendParam["min"]+legendParam["step size"]*i):
            i += 1
        return i-1
    
    # Create all materials for meshes based on legend colors
    def createAllMats(legendColors, matFolder):
        #defining values of material properties
        ior = 1.0
        transmWeight = 0.85
        rough = 1.0

        for i in range(len(legendColors)):
            # Create material
            omni.kit.commands.execute('CreateMdlMaterialPrim',
                                    mtl_url='OmniSurface.mdl',
                                    mtl_name='OmniSurface',
                                    mtl_path=Func.getPath(matFolder) + '/mat' + str(i),
                                    select_new_prim=False)
            # Change material properties
            mtl_prim = Func.getPrimAtPath(Func.getPath(matFolder) + '/mat' + str(i))
            omni.usd.create_material_input(mtl_prim, "diffuse_reflection_color", legendColors[i], Sdf.ValueTypeNames.Color3f)
            omni.usd.create_material_input(mtl_prim, "specular_reflection_ior", ior, Sdf.ValueTypeNames.Float)
            omni.usd.create_material_input(mtl_prim, "enable_specular_transmission", True, Sdf.ValueTypeNames.Bool)
            omni.usd.create_material_input(mtl_prim, "specular_transmission_weight", transmWeight, Sdf.ValueTypeNames.Float)
            omni.usd.create_material_input(mtl_prim, "specular_reflection_roughness", rough, Sdf.ValueTypeNames.Float)
    # ----------------------------------------------------#
    # Functions to assign meshes the appropriate material #
    # ----------------------------------------------------#
    # Assign material to visualize energy results to all selected meshes
    def assign_all_mats(matFolder, legendColors, dataToRead):
        selected_prims = Func.getSelPaths()
        legendParam = LegendOverlay.makeLegendParam(selected_prims, legendColors, dataToRead)
        for s in selected_prims:
            # determine if s is prim or layer and act accordingly 
            curr_prim = Func.getPrimAtPath(s)
            if len(curr_prim.GetChildren())==0:
                color = AssignMat.determColorIndex(curr_prim, legendParam, dataToRead) 
                volmFolder = Func.getPrimAtPath('/World/Energy_Results/ColoredVolms')           
                AssignMat.assign_material(s, color, volmFolder, matFolder)
                dataIndex += 1
            else:
                volmFolder = Func.defineXform('/World/Energy_Results/ColoredVolms/' + curr_prim.GetName())
                dataIndex = AssignMat.assign_one_layer_mats(curr_prim.GetChildren(), volmFolder, matFolder, legendParam, dataToRead)
            # make original selection invisible to better view energy results
            Func.invisible([s])

    # Recursively assign mats for one layer
    def assign_one_layer_mats(children, volmFolder, matFolder, legendParam, dataToRead):
        if len(children)==0:
            return
        for c in children:
                if len(c.GetChildren()) == 0:
                    # Determine color of the prim, 
                    # assign a copied prim a transparent material of that color
                    color = AssignMat.determColorIndex(c, legendParam, dataToRead)                
                    AssignMat.assign_material(Func.getPath(c), color, volmFolder, matFolder)
                else:
                    # c is a layer so create a folder in energy Results for that layer then traverse it
                    subVolmFolder = Func.defineXform(Func.getPath(volmFolder) + '/' + c.GetName())
                    AssignMat.assign_one_layer_mats(c.GetChildren(), subVolmFolder, matFolder, legendParam, dataToRead)

    # Assign material to one prim
    def assign_material(prim_path, colorIndex, volmsFolder, matFolder):
        #copy prim
        omni.kit.commands.execute('CopyPrim',
                                path_from=prim_path,
                                path_to=prim_path+'ColoredVolm',
                                exclusive_select=False)
        #change selected prim paths from selected layer to this copied prim to bind material
        Func.setSelPaths([prim_path+"ColoredVolm"])
        #get the created material
        mtl_prim = Func.getPrimAtPath(Func.getPath(matFolder) + '/mat' + str(colorIndex))

        # Get the path to the prim
        prim = Func.getPrimAtPath(prim_path+'ColoredVolm')
        prim_name = prim.GetName()
        # Bind the material to the prim
        mat_shade = UsdShade.Material(mtl_prim)
        UsdShade.MaterialBindingAPI(prim).Bind(mat_shade, UsdShade.Tokens.strongerThanDescendants)
        # Move colored volume to the appropriate folder
        omni.kit.commands.execute('MovePrim',
                                path_from=prim_path+'ColoredVolm',
                                path_to=Func.getPath(volmsFolder) + '/' + prim_name)  
    