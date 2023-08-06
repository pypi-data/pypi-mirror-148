import PseudoNetCDF as pnc
import numpy as np

path='https://aura.gesdisc.eosdis.nasa.gov/opendap/hyrax/Aura_OMI_Level2/OMNO2.003/2020/001/OMI-Aura_L2-OMNO2_2020m0101t0117-o82246_v003-2020m0610t191058.he5'

key = 'CloudFraction'
satf = pnc.pncopen(path, format='netcdf')
#satf.set_auto_maskandscale(False)
subsetf = satf.subset([key])
copyf = pnc.PseudoNetCDFFile()
copyf.copyDimension(satf.dimensions['nTimes'], key='nTimes')
copyf.copyDimension(satf.dimensions['nXtrack'], key='nXtrack')
copyf.copyVariable(satf.variables[key], key=key)
print('Bad', np.unique(subsetf.variables[key][:]))
print('Good', np.unique(copyf.variables[key][:]))
print('Good', np.unique(satf.variables[key][:]))
