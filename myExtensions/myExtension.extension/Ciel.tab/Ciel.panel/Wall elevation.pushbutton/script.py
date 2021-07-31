"""Create an elevation view for all the walls in the model"""
from Autodesk.Revit import DB
from Autodesk.Revit.DB import *
doc = __revit__.ActiveUIDocument.Document
# Creating collector instance and collecting all the walls from the model
wall_collector = DB.FilteredElementCollector(doc)\
                   .OfCategory(BuiltInCategory.OST_Walls)\
                   .WhereElementIsNotElementType()
#get ViewFamilyType for a Section View
collector = DB.FilteredElementCollector(doc)
viewTypeColl = collector.OfClass(ViewFamilyType)
for i in viewTypeColl:
	if i.ViewFamily == ViewFamily.Section:
		viewType = i
	else:
		continue

#create an elevation view for all the walls.
for wall in wall_collector:
     lc = wall.Location
     line = lc.Curve 
     p = line.GetEndPoint(0)
     q = line.GetEndPoint(1)
     v = q - p
     bb = wall.get_BoundingBox(None)
     minZ = bb.Min.Z
     maxZ = bb.Max.Z
     w = v.GetLength()
     h = maxZ - minZ
     d = wall.WallType.Width
     offset = 0.1 * w
     minPoint = XYZ( -0.5*w, minZ ,0)
     maxPoint = XYZ( 0.5*w, maxZ , 0.5*d)
     midpoint = p + 0.5 * v
     walldir = v.Normalize()
     up = XYZ.BasisZ
     viewdir = walldir.CrossProduct(up)
 
     t = Transform.Identity
     t.Origin = midpoint
     t.BasisX = walldir
     t.BasisY = up
     t.BasisZ = viewdir
 
     sectionBox = BoundingBoxXYZ()
     sectionBox.Transform = t
     sectionBox.Min = minPoint
     sectionBox.Max = maxPoint
     t = Transaction(doc, "Create view sections")
     t.Start()
     try:
          ViewSection.CreateSection(doc,viewType.Id,sectionBox)
     except:
          print("error")
     t.Commit()
 
    


