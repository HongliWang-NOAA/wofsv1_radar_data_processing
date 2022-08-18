import netCDF4 as nc
import numpy as np
import time
from ..sparsey import sparse_decompress

def decompress_sparse(a, method = 'f'):
    t0 = time.perf_counter()

    # Gather into four arrays
    var = a.variables[a.TypeName][:]
    pixel_x = a.variables['pixel_x'][:]
    pixel_y = a.variables['pixel_y'][:]
    pixel_count = a.variables['pixel_count'][:]

    if not (len(var) > 0 and len(var) == len(pixel_x) == len(pixel_y) == len(pixel_count)):
        return None

    if method == 'f':
        b = __decompress_sparse_f__(a, var, pixel_x, pixel_y, pixel_count)
    elif method == 'py':
        b = __decompress_sparse_py__(a, var, pixel_x, pixel_y, pixel_count)
    else: 
        b = __decompress_sparse_loop__(a, var, pixel_x, pixel_y, pixel_count)
    
    t1 = time.perf_counter()
    print('Time to decompress (method %s): %f' % (method, t1 - t0))    

    return b

def __decompress_sparse_f__(a, var, pixel_x, pixel_y, pixel_count):
    """This expands a sparse grid, incorporating all data values"""
    return sparse_decompress(var, pixel_x, pixel_y, pixel_count, len(a.dimensions['Azimuth']), len(a.dimensions['Gate']), -99900.)

def __decompress_sparse_py__(a, var, pixel_x, pixel_y, pixel_count):
    """This expands a sparse grid, incorporating all data values"""

    # Create empty shape for filling
    b = np.full([len(a.dimensions['Azimuth']),len(a.dimensions['Gate'])], -99900.)

    for w,x,y,z in zip(var, pixel_x, pixel_y, pixel_count):
        __set_grid_data__(b,w,x,y,z)

    return b

def __set_grid_data__(array, value, x, y, z):
    distToEdge = array.shape[1] - y
    # check if pixel count exceeds distance to right edge of domain
    if z > distToEdge:
        array[x,y:array.shape[1]] = value
        # drop to next row and continue
        __set_grid_data__(array, value, x + 1, 0, z - distToEdge)
    else:
        array[x,y:(y + z)] = value

def __decompress_sparse_loop__(a, var, pixel_x, pixel_y, pixel_count):
    """This expands a sparse grid, incorporating all data values"""

    # Create empty shape for filling
    b = np.full([len(a.dimensions['Azimuth']),len(a.dimensions['Gate'])], -99900.)

    # Create empty shape for filling
    xlen = b.shape[0]
    ylen = b.shape[1]

    #Loop through the four arrays simultaneously, populating 2D array 'b'
    for w,x,y,z in zip(var, pixel_x, pixel_y, pixel_count):
        distToEdge = ylen - y
        # check if pixel count exceeds distance to right edge of domain
        if z > distToEdge:
            b[x,y:ylen] = w
            pixelsLeft = z - distToEdge
            # check if pixels remaining are less than grid width
            if pixelsLeft <= xlen:
                b[x+1,0:(pixelsLeft-1)] = w
            else:
                rowsLeft, pixelCount_RemainingRow = divmod(pixelsLeft, xlen)
                b[x:(x+rowsLeft+1),0:7001] = w
                # check if pixels are remaining
                if pixelCount_RemainingRow > 0:
                    b[(x+rowsLeft+1),0:pixelCount_RemainingRow] = w
        else:
            b[x,y:(y + z)] = w

    return b

def read_wdssii(fin):

    """This loads in the file"""

    a = nc.Dataset(fin, 'r')

    xlen = len(a.dimensions['Azimuth'])
    ylen = len(a.dimensions['Gate'])
    lat = a.Latitude
    lon = a.Longitude
    try:
        varname = a.TypeName


        var = a.variables[varname][:]

        if a.DataType[0:6] == 'Sparse':

            var = sparseFull(a)

    except:
        print('except')
        return xlen,ylen,varname,0
    a.close()
    del(a)

    return xlen, lat, ylen, lon, varname, var


# ###CODE HERE
# ####can loop over this...
# x1,ulat,y1,ulon, varname,ref1 = readwdssii('/Users/aereinha/Downloads/RotationTracks60min/00.50/20170528-235400.netcdf')


# #longitude runs west to east
# #latitude runs north to south
# lat = np.linspace(ulat,stop=ulat+(y1*-0.01),num=y1)
# lon = np.linspace(ulon,stop=ulon+(x1*0.01),num=x1)
# nx,ny = np.meshgrid(lon,lat)
# fig = plt.figure()
# #ulat is upper corner, lon[-1] is lower corner lat[-1] is upper and ulat is lower
# m = Basemap(resolution = 'l',llcrnrlat=lat[-1],llcrnrlon=ulon,urcrnrlat=ulat,urcrnrlon=lon[-1],projection='lcc',lat_0=38.0,lon_0=-97)

# xx,yy = m(nx,ny)
# #need to divide AzShear by 1000 because of scaling...
# m.contourf(xx,yy,ref1,levels=np.arange(0,70,10),cmap=get_cmap('viridis'))
# plt.colorbar()
# m.drawstates()
# m.drawcountries()
# m.drawcoastlines()
# plt.show()
