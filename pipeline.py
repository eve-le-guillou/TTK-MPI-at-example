# state file generated using paraview version 5.11.0
import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 11
from time import time

#### import the simple module from the paraview
from paraview.simple import *

# ----------------------------------------------------------------
# Choose the resampling dimension for the example
# ----------------------------------------------------------------

if len(sys.argv) == 2:
        dim = int(sys.argv[1])
else:
        dim = 256

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [1238, 778]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.OrientationAxesVisibility = 0
renderView1.OrientationAxesOutlineColor = [0.5019607843137255, 0.4901960784313725, 0.4901960784313725]
renderView1.CenterOfRotation = [88.0, 47.0, 23.5]
renderView1.Exposure = 1.5
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [70.89683975693343, 17.071617299486153, -197.36397333253876]
renderView1.CameraFocalPoint = [88.00000000000028, 47.000000000000185, 23.499999999999705]
renderView1.CameraViewUp = [-0.013891462386409929, -0.990704280371448, 0.13532204597351677]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 102.49512183513906
renderView1.UseColorPaletteForBackground = 0
renderView1.Background = [1.0, 1.0, 1.0]

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.Visibility = 1
renderView1.AxesGrid.XTitle = 'Birth'
renderView1.AxesGrid.YTitle = 'Death'
renderView1.AxesGrid.ZTitle = ''
renderView1.AxesGrid.GridColor = [0.2823529411764706, 0.2784313725490196, 0.2784313725490196]
renderView1.AxesGrid.ShowEdges = 0
renderView1.AxesGrid.ShowTicks = 0
renderView1.AxesGrid.AxesToLabel = 0

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(1238, 778)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

t0 = time()
# create a new 'XML Image Data Reader'
atvti = XMLImageDataReader(registrationName='at.vti', FileName=['./at.vti'])
atvti.PointArrayStatus = ['density']
atvti.TimeArray = 'None'

calculator1 = Calculator(registrationName='Calculator1', Input=atvti)
calculator1.Function = ''
calculator1.ResultArrayType = 'Float'

# Properties modified on calculator1
calculator1.ResultArrayName = 'density'
calculator1.Function = 'density'

# create a new 'Compute Derivatives'
computeDerivatives1 = ComputeDerivatives(registrationName='ComputeDerivatives1', Input=calculator1)
computeDerivatives1.Scalars = ['POINTS', 'density']
computeDerivatives1.Vectors = ['POINTS', '1']

# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=computeDerivatives1)
calculator2.AttributeType = 'Cell Data'
calculator2.ResultArrayName = 'gradientMagnitude'
calculator2.Function = 'mag(ScalarGradient)'
calculator2.ResultArrayType = 'Float'

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=calculator2)
cellDatatoPointData1.CellDataArraytoprocess = ['gradientMagnitude']

# create a new 'TTK PointDataSelector'
tTKPointDataSelector1 = TTKPointDataSelector(registrationName='TTKPointDataSelector1', Input=cellDatatoPointData1)
tTKPointDataSelector1.ScalarFields = ['density', 'gradientMagnitude']
tTKPointDataSelector1.RangeId = [0, 2]

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=tTKPointDataSelector1)
cellDatatoPointData1.CellDataArraytoprocess = ['ScalarGradient', 'gradientMagnitude']

# create a new 'Resample To Image'
resampleToImage1 = ResampleToImage(registrationName='ResampleToImage1', Input=cellDatatoPointData1)
resampleToImage1.SamplingDimensions = [dim, dim, dim]
resampleToImage1.SamplingBounds = [0.0, 176.0, 0.0, 94.0, 0.0, 47.0]

UpdatePipeline(proxy=resampleToImage1)
t1 = time()

# create a new 'TTK ScalarFieldSmoother'
tTKScalarFieldSmoother1 = TTKScalarFieldSmoother(registrationName='TTKScalarFieldSmoother1', Input=resampleToImage1)
tTKScalarFieldSmoother1.ScalarField = ['POINTS', 'density']
tTKScalarFieldSmoother1.IterationNumber = 1
tTKScalarFieldSmoother1.MaskField = ['POINTS', 'gradientMagnitude']

# create a new 'TTK ScalarFieldSmoother'
tTKScalarFieldSmoother2 = TTKScalarFieldSmoother(registrationName='TTKScalarFieldSmoother2', Input=tTKScalarFieldSmoother1)
tTKScalarFieldSmoother2.ScalarField = ['POINTS', 'gradientMagnitude']
tTKScalarFieldSmoother2.IterationNumber = 10
tTKScalarFieldSmoother2.MaskField = ['POINTS', 'gradientMagnitude']

# create a new 'TTK ScalarFieldNormalizer'
tTKScalarFieldNormalizer2 = TTKScalarFieldNormalizer(registrationName='TTKScalarFieldNormalizer2', Input=tTKScalarFieldSmoother2)
tTKScalarFieldNormalizer2.ScalarField = ['POINTS', 'density']

# create a new 'TTK ArrayPreconditioning'
tTKArrayPreconditioning1 = TTKArrayPreconditioning(registrationName='TTKArrayPreconditioning1', Input=tTKScalarFieldNormalizer2)
tTKArrayPreconditioning1.PointDataArrays = ['density']

# create a new 'TTK ScalarFieldCriticalPoints'
tTKScalarFieldCriticalPoints2 = TTKScalarFieldCriticalPoints(registrationName='TTKScalarFieldCriticalPoints2', Input=tTKArrayPreconditioning1)
tTKScalarFieldCriticalPoints2.ScalarField = ['POINTS', 'density']
tTKScalarFieldCriticalPoints2.InputOffsetField = ['POINTS', 'gradientMagnitude']
tTKScalarFieldCriticalPoints2.Backend = 'Default generic backend'

# create a new 'Mask Points'
maskPoints2 = MaskPoints(registrationName='MaskPoints2', Input=tTKScalarFieldCriticalPoints2)
maskPoints2.OnRatio = 1
maskPoints2.MaximumNumberofPoints = 99999999
maskPoints2.ProportionallyDistributeMaximumNumberOfPoints = 1
maskPoints2.RandomSampling = 1
maskPoints2.RandomSamplingMode = 'Random Sampling'
maskPoints2.GenerateVertices = 1
maskPoints2.SingleVertexPerCell = 1

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=maskPoints2)
threshold1.Scalars = ['POINTS', 'CriticalType']
threshold1.LowerThreshold = 1.0
threshold1.UpperThreshold = 1.0

# create a new 'Threshold'
threshold4 = Threshold(registrationName='Threshold4', Input=threshold1)
threshold4.Scalars = ['POINTS', 'IsOnBoundary']

# create a new 'TTK IcospheresFromPoints'
tTKIcospheresFromPoints1 = TTKIcospheresFromPoints(registrationName='TTKIcospheresFromPoints1', Input=threshold4)
tTKIcospheresFromPoints1.Radius = 1.75

# create a new 'TTK IntegralLines'
tTKIntegralLines1 = TTKIntegralLines(registrationName='TTKIntegralLines1', Domain=tTKArrayPreconditioning1,
    Seeds=threshold4)
tTKIntegralLines1.ScalarField = ['POINTS', 'density']
tTKIntegralLines1.Direction = 'Backward'
tTKIntegralLines1.Vertexidentifierfield = ['POINTS', 'CriticalType']
tTKIntegralLines1.InputOffsetField = ['POINTS', 'gradientMagnitude']
tTKIntegralLines1.EnableForking = 1

# create a new 'Clean to Grid'
cleantoGrid1 = CleantoGrid(registrationName='CleantoGrid1', Input=tTKIntegralLines1)

# create a new 'TTK GeometrySmoother'
tTKGeometrySmoother2 = TTKGeometrySmoother(registrationName='TTKGeometrySmoother2', Input=cleantoGrid1)
tTKGeometrySmoother2.IterationNumber = 200
tTKGeometrySmoother2.InputMaskField = ['POINTS', 'DistanceFromSeed']

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(registrationName='ResampleWithDataset1', SourceDataArrays=cellDatatoPointData1,
    DestinationMesh=tTKGeometrySmoother2)
resampleWithDataset1.CellLocator = 'Static Cell Locator'
resampleWithDataset1.PassCellArrays = 1
resampleWithDataset1.PassPointArrays = 1

# create a new 'TTK ScalarFieldCriticalPoints'
tTKScalarFieldCriticalPoints1 = TTKScalarFieldCriticalPoints(registrationName='TTKScalarFieldCriticalPoints1', Input=resampleWithDataset1)
tTKScalarFieldCriticalPoints1.ScalarField = ['POINTS', 'gradientMagnitude']
tTKScalarFieldCriticalPoints1.InputOffsetField = ['POINTS', 'gradientMagnitude']
tTKScalarFieldCriticalPoints1.Backend = 'Default generic backend'

# create a new 'TTK IcospheresFromPoints'
tTKIcospheresFromPoints2 = TTKIcospheresFromPoints(registrationName='TTKIcospheresFromPoints2', Input=tTKScalarFieldCriticalPoints1)

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=tTKGeometrySmoother2)
extractSurface1.PieceInvariant = 0

# create a new 'Tube'
tube1 = Tube(registrationName='Tube1', Input=extractSurface1)
tube1.Scalars = ['POINTS', 'gradientMagnitude']
tube1.Vectors = ['POINTS', '1']
tube1.Radius = 0.3

# create a new 'Contour'
contour2 = Contour(registrationName='Contour2', Input=cellDatatoPointData1)
contour2.ContourBy = ['POINTS', '']
contour2.Isosurfaces = [0.08902849535643777]
contour2.PointMergeMethod = 'Uniform Binning'

# create a new 'Contour'
contour1 = Contour(registrationName='Contour1', Input=atvti)
contour1.ContourBy = ['POINTS', 'density']
contour1.Isosurfaces = [-1.0]
contour1.PointMergeMethod = 'Uniform Binning'

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from contour1
contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'density'
densityLUT = GetColorTransferFunction('density')
densityLUT.RGBPoints = [-3.7645358731683567, 0.929412, 1.0, 1.0, -2.220358669712149, 0.439216, 0.611765, 0.729412, -0.6761814662559389, 0.235294, 0.333333, 0.501961, 0.8679957372002702, 0.066667, 0.078431, 0.2, 1.3914013696870091, 0.2, 0.1, 0.2, 1.877483094034881, 0.4, 0.039216, 0.058824, 3.184328456730066, 0.890196, 0.411765, 0.019608, 5.243190216612917, 0.968627, 0.905882, 0.486275, 6.529978816539702, 1.0, 1.0, 0.7]
densityLUT.ColorSpace = 'Lab'
densityLUT.NanColor = [0.0, 0.0, 0.0]
densityLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
contour1Display.Representation = 'Surface'
contour1Display.AmbientColor = [0.5019607843137255, 0.4901960784313725, 0.4901960784313725]
contour1Display.ColorArrayName = ['POINTS', '']
contour1Display.LookupTable = densityLUT
contour1Display.Opacity = 0.2
contour1Display.Specular = 1.0
contour1Display.SelectTCoordArray = 'None'
contour1Display.SelectNormalArray = 'Normals'
contour1Display.SelectTangentArray = 'None'
contour1Display.SelectOrientationVectors = 'None'
contour1Display.ScaleFactor = 15.944606685638428
contour1Display.SelectScaleArray = 'density'
contour1Display.GlyphType = 'Arrow'
contour1Display.GlyphTableIndexArray = 'density'
contour1Display.GaussianRadius = 0.7972303342819214
contour1Display.SetScaleArray = ['POINTS', 'density']
contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
contour1Display.OpacityArray = ['POINTS', 'density']
contour1Display.OpacityTransferFunction = 'PiecewiseFunction'
contour1Display.DataAxesGrid = 'GridAxesRepresentation'
contour1Display.PolarAxes = 'PolarAxesRepresentation'
contour1Display.SelectInputVectors = [None, '']
contour1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
contour1Display.ScaleTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, -0.9998779296875, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
contour1Display.ScaleTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, -0.9998779296875, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
contour1Display.OpacityTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, -0.9998779296875, 1.0, 0.5, 0.0]

# show data from tTKIcospheresFromPoints1
tTKIcospheresFromPoints1Display = Show(tTKIcospheresFromPoints1, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'CriticalType'
criticalTypeLUT = GetColorTransferFunction('CriticalType')
criticalTypeLUT.TransferFunction2D = None
criticalTypeLUT.RGBPoints = [0.0, 0.929412, 1.0, 1.0, 0.6, 0.439216, 0.611765, 0.729412, 1.2, 0.235294, 0.333333, 0.501961, 1.8, 0.066667, 0.078431, 0.2, 2.0033726302843644, 0.2, 0.1, 0.2, 2.1922428156205735, 0.4, 0.039216, 0.058824, 2.7000260000000003, 0.890196, 0.411765, 0.019608, 3.50001, 0.968627, 0.905882, 0.486275, 4.0, 1.0, 1.0, 0.7]
criticalTypeLUT.ColorSpace = 'Lab'
criticalTypeLUT.NanColor = [0.0, 0.0, 0.0]
criticalTypeLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
tTKIcospheresFromPoints1Display.Representation = 'Surface'
tTKIcospheresFromPoints1Display.AmbientColor = [0.1803921568627451, 0.17647058823529413, 0.17647058823529413]
tTKIcospheresFromPoints1Display.ColorArrayName = ['POINTS', 'CriticalType']
tTKIcospheresFromPoints1Display.DiffuseColor = [0.1803921568627451, 0.17647058823529413, 0.17647058823529413]
tTKIcospheresFromPoints1Display.LookupTable = criticalTypeLUT
tTKIcospheresFromPoints1Display.Opacity = 0.3
tTKIcospheresFromPoints1Display.Specular = 1.0
tTKIcospheresFromPoints1Display.SelectTCoordArray = 'None'
tTKIcospheresFromPoints1Display.SelectNormalArray = 'Normals'
tTKIcospheresFromPoints1Display.SelectTangentArray = 'None'
tTKIcospheresFromPoints1Display.SelectOrientationVectors = 'None'
tTKIcospheresFromPoints1Display.ScaleFactor = 12.350000000000001
tTKIcospheresFromPoints1Display.SelectScaleArray = 'CriticalType'
tTKIcospheresFromPoints1Display.GlyphType = 'Arrow'
tTKIcospheresFromPoints1Display.GlyphTableIndexArray = 'CriticalType'
tTKIcospheresFromPoints1Display.GaussianRadius = 0.6175
tTKIcospheresFromPoints1Display.SetScaleArray = ['POINTS', 'CriticalType']
tTKIcospheresFromPoints1Display.ScaleTransferFunction = 'PiecewiseFunction'
tTKIcospheresFromPoints1Display.OpacityArray = ['POINTS', 'CriticalType']
tTKIcospheresFromPoints1Display.OpacityTransferFunction = 'PiecewiseFunction'
tTKIcospheresFromPoints1Display.DataAxesGrid = 'GridAxesRepresentation'
tTKIcospheresFromPoints1Display.PolarAxes = 'PolarAxesRepresentation'
tTKIcospheresFromPoints1Display.SelectInputVectors = [None, '']
tTKIcospheresFromPoints1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
tTKIcospheresFromPoints1Display.ScaleTransferFunction.Points = [1.0, 0.0, 0.5, 0.0, 1.000244140625, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
tTKIcospheresFromPoints1Display.OpacityTransferFunction.Points = [1.0, 0.0, 0.5, 0.0, 1.000244140625, 1.0, 0.5, 0.0]

# show data from tTKIcospheresFromPoints2
tTKIcospheresFromPoints2Display = Show(tTKIcospheresFromPoints2, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
tTKIcospheresFromPoints2Display.Representation = 'Surface'
tTKIcospheresFromPoints2Display.ColorArrayName = ['POINTS', 'CriticalType']
tTKIcospheresFromPoints2Display.LookupTable = criticalTypeLUT
tTKIcospheresFromPoints2Display.SelectTCoordArray = 'None'
tTKIcospheresFromPoints2Display.SelectNormalArray = 'Normals'
tTKIcospheresFromPoints2Display.SelectTangentArray = 'None'
tTKIcospheresFromPoints2Display.SelectOrientationVectors = 'None'
tTKIcospheresFromPoints2Display.ScaleFactor = 15.200000000000001
tTKIcospheresFromPoints2Display.SelectScaleArray = 'CriticalType'
tTKIcospheresFromPoints2Display.GlyphType = 'Arrow'
tTKIcospheresFromPoints2Display.GlyphTableIndexArray = 'CriticalType'
tTKIcospheresFromPoints2Display.GaussianRadius = 0.76
tTKIcospheresFromPoints2Display.SetScaleArray = ['POINTS', 'CriticalType']
tTKIcospheresFromPoints2Display.ScaleTransferFunction = 'PiecewiseFunction'
tTKIcospheresFromPoints2Display.OpacityArray = ['POINTS', 'CriticalType']
tTKIcospheresFromPoints2Display.OpacityTransferFunction = 'PiecewiseFunction'
tTKIcospheresFromPoints2Display.DataAxesGrid = 'GridAxesRepresentation'
tTKIcospheresFromPoints2Display.PolarAxes = 'PolarAxesRepresentation'
tTKIcospheresFromPoints2Display.SelectInputVectors = ['POINTS', 'Normals']
tTKIcospheresFromPoints2Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
tTKIcospheresFromPoints2Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 3.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
tTKIcospheresFromPoints2Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 3.0, 1.0, 0.5, 0.0]

# get color transfer function/color map for 'gradientMagnitude'
gradientMagnitudeLUT = GetColorTransferFunction('gradientMagnitude')
gradientMagnitudeLUT.TransferFunction2D = None
gradientMagnitudeLUT.RGBPoints = [1e-06, 0.929412, 1.0, 1.0, 0.15000099999999997, 0.439216, 0.611765, 0.729412, 0.3000009999999999, 0.235294, 0.333333, 0.501961, 0.45000099999999993, 0.066667, 0.078431, 0.2, 0.500844157571091, 0.2, 0.1, 0.2, 0.5480617039051433, 0.4, 0.039216, 0.058824, 0.6750075, 0.890196, 0.411765, 0.019608, 0.8750034999999999, 0.968627, 0.905882, 0.486275, 1.000001, 1.0, 1.0, 0.7]
gradientMagnitudeLUT.ColorSpace = 'Lab'
gradientMagnitudeLUT.NanColor = [0.0, 0.0, 0.0]
gradientMagnitudeLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# show data from tube1
tube1Display = Show(tube1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
tube1Display.Representation = 'Surface'
tube1Display.ColorArrayName = ['POINTS', 'gradientMagnitude']
tube1Display.LookupTable = gradientMagnitudeLUT
tube1Display.SelectTCoordArray = 'None'
tube1Display.SelectNormalArray = 'TubeNormals'
tube1Display.SelectTangentArray = 'None'
tube1Display.SelectOrientationVectors = 'None'
tube1Display.ScaleFactor = 15.00286865234375
tube1Display.SelectScaleArray = 'DistanceFromSeed'
tube1Display.GlyphType = 'Arrow'
tube1Display.GlyphTableIndexArray = 'DistanceFromSeed'
tube1Display.GaussianRadius = 0.7501434326171875
tube1Display.SetScaleArray = ['POINTS', 'DistanceFromSeed']
tube1Display.ScaleTransferFunction = 'PiecewiseFunction'
tube1Display.OpacityArray = ['POINTS', 'DistanceFromSeed']
tube1Display.OpacityTransferFunction = 'PiecewiseFunction'
tube1Display.DataAxesGrid = 'GridAxesRepresentation'
tube1Display.PolarAxes = 'PolarAxesRepresentation'
tube1Display.SelectInputVectors = ['POINTS', 'TubeNormals']
tube1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
tube1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 23.242640614509583, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
tube1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 23.242640614509583, 1.0, 0.5, 0.0]

# get opacity transfer function/opacity map for 'gradientMagnitude'
gradientMagnitudePWF = GetOpacityTransferFunction('gradientMagnitude')
gradientMagnitudePWF.Points = [1e-06, 0.0, 0.5, 0.0, 1.000001, 1.0, 0.5, 0.0]
gradientMagnitudePWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'CriticalType'
criticalTypePWF = GetOpacityTransferFunction('CriticalType')
criticalTypePWF.Points = [0.0, 0.0, 0.5, 0.0, 4.0, 1.0, 0.5, 0.0]
criticalTypePWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'density'
densityPWF = GetOpacityTransferFunction('density')
densityPWF.Points = [-3.7645358731683567, 1.0, 0.5, 0.0, -1.7128952741622925, 0.1026785746216774, 0.5, 0.0, -1.0048069953918457, 0.0, 0.5, 0.0, 0.17616011873621584, 0.0, 0.5, 0.0, 6.529978816539702, 0.0, 0.5, 0.0]
densityPWF.ScalarRangeInitialized = 1
t2 = time()
SaveScreenshot("atExample.png",renderView1, ImageResolution=[1280, 720])
t3 = time()
print(f"Loading file and resampling time: {t1-t0}")
print(f"Pipeline time: {t2 - t1}")
print(f"File saving time: {t3 - t2}")
print(f"Total time: {t3 - t0}")
