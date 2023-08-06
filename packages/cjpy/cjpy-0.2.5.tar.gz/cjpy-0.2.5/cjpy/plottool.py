
# Jaesub Hong (jhong@cfa.harvard.edu)

import cjson
from collections import OrderedDict

import pandas
import astropy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm	 as cm
import matplotlib		 as mpl
from matplotlib.patches		import Circle
from matplotlib			import rc,rcParams
from mpl_toolkits.axes_grid1  import make_axes_locatable

import tabletool as tt
import numpy as np
import math

from astropy.io import fits

from scipy import optimize as opt
from scipy import ndimage

from os		import path
from IPython	import embed

def add_margin(prange, margin=None, scale='linear', drawdown=None):

	if   margin == None     : margin=[0.2,0.2]
	elif np.isscalar(margin): margin=[margin, margin]
	if scale == 'linear':
		diff=prange[1]-prange[0]
		prange=[prange[0]-margin[0]*diff,prange[1]+margin[1]*diff]
	else:
		if prange[0] <= 0.0:
			if drawdown == None: drawdown = 1.e-5
			prange[0]=prange[1]*drawdown

		logpr = [math.log(v,10) for v in prange]
		diff = logpr[1]-logpr[0]
		logpr=[logpr[0]-margin[0]*diff,logpr[1]+margin[1]*diff]
		prange=[10.0**v for v in logpr]

	return prange

def read(infile, x=None, y=None, hdu=1, data=None,
		xlabel=None, ylabel=None,
		ftype=None, nopandas=True):
	if str(type(data)) == "<class 'NoneType'>":
		if infile == None: 
			print("input data or file is required.")
			return None, None, None, None, None, None, None

		if not path.isfile(infile):
			print("cannot read the file:", infile)
			return None, None, None, None, None, None, None

		data=tt.from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if x == None or y == None:
		if   type(data) is pandas.core.frame.DataFrame: colnames=data.columns.values.tolist()
		elif type(data) is   astropy.table.table.Table: colnames=data.colnames
		else: print('need to know column names or provide -x and -y')

#		colnames=data.colnames
		if x == None: x=colnames[0]
		if y == None: y=colnames[1]
	
	# default label
	if xlabel == None:
		xlabel = x 
		if hasattr(data[x],'info'):
			if hasattr(data[x].info,'unit'):
				xunit=data[x].info,'unit'
				if xunit != None: xlabel = xlabel +' ('+str(xunit)+')'

	if ylabel == None:
		ylabel = y 
		if hasattr(data[y],'info'):
			if hasattr(data[y].info,'unit'):
				yunit=data[y].info.unit
				if yunit != None: ylabel = ylabel +' ('+str(yunit)+')'
	return data, x, y, xlabel, ylabel
	
def set_range(xdata, ydata, margin=None, xr=None, yr=None, 
		xscale='linear', yscale='linear', drawdown=None):

#	embed()
	if type(xr) is list: 
		if xr[0] == None: xr = None
	if type(yr) is list: 
		if yr[0] == None: yr = None
	if xr == None: xr= cjson.minmax(xdata, nonzero= xscale != 'linear')
	if yr == None: yr= cjson.minmax(ydata, nonzero= yscale != 'linear')

	if margin != None:
		if type(margin) is not list:
			xr = add_margin(xr, margin=margin, scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin, scale=yscale, drawdown=drawdown)
		elif len(margin) == 2:
			xr = add_margin(xr, margin=margin[0], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[1], scale=yscale, drawdown=drawdown)
		elif len(margin) == 4:
			xr = add_margin(xr, margin=margin[0:1], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[2:3], scale=yscale, drawdown=drawdown)

	return xr, yr

def filter_by_range(xdata, ydata, xr, yr):
	mask = xdata >= xr[0] and xdata <= xr[1] and ydata >= yr[0] and ydata <= yr[1] 
	xdata=xdata[mask]
	ydata=ydata[mask]
#	if filter:
#		 data=data[data[x] >= xr[0]]
#		 data=data[data[x] <= xr[1]]
#		 data=data[data[y] >= yr[0]]
#		 data=data[data[y] <= yr[1]]

	return xdata, ydata

def wrap(plt, xr, yr, xlabel, ylabel, title="", xscale='linear', yscale='linear', outfile=None, 
		display=True, ion=False):
	plt.xlim(xr)
	plt.ylim(yr)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.xscale(xscale)
	plt.yscale(yscale)
	plt.tight_layout()
	if not ion: 
		if outfile != None: plt.savefig(outfile)
		else: 
			if display: plt.show()

def get_log_edges(vr, nbin):
	logvr = [math.log(vr[0],10), math.log(vr[1],10)]
	logslope = logvr[1] - logvr[0]
	return [10.0**(logslope*v/nbin+logvr[0]) for v in range(0,nbin+1)]

#----------------------------------------------------------------------------------------
def plot1d(xdata, ydata, data=None, 
		infile=None, outfile=None, x=None, y=None, 
		margin=None,
		xr=None, yr=None, filter=False, drawdown=None,
		xscale='linear', yscale='linear',
		xlabel=None, ylabel=None,
		hold=True, hdu=1, ftype=None):
	"""Plot 1-D from input table
	"""
	if str(type(xdata)) == "<class 'NoneType'>":
		data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data, 
				xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu)
		if str(type(data)) == "<class 'NoneType'>": return False

		xdata=data[x]
		ydata=data[y]

	if xscale == None: 
		xscale = 'log' if xlog else 'linear'
	if yscale == None: 
		yscale = 'log' if ylog else 'linear'

	xr, yr =  set_range(xdata, ydata, xr=xr, yr=yr, 
			margin=margin, drawdown=drawdown,
			xscale=xscale, yscale=yscale)
	if filter:
		xdata, ydata = filter_by_range(xdata, ydata, xr, yr)

	def show(ion=True):
		if ion: plt.ion()
		plt.plot(data[x], data[y])

		wrap(plt, xr, yr, xlabel, ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, ion=ion)

	show(ion=False)
	if hold: embed()

	return plt

def dplot(xdata, ydata, data=None, 
		infile=None, outfile=None, 
		x=None, y=None, 
		margin=None,
		xr=None, yr=None, filter=False, drawdown=None,
		xscale=None, yscale=None,
		xlog=False, ylog=False,
		xlabel=None, ylabel=None, title=None,
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, zmin=0,
		cmap='Blues', aspect='auto',
		interpolation=None,
		display=True,
		hold=True, hdu=1, ftype=None
		):

	if str(type(xdata)) == "<class 'NoneType'>":
		data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data, 
				xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu)
		if str(type(data)) == "<class 'NoneType'>": return False

		xdata=data[x]
		ydata=data[y]

	if xscale == None: 
		xscale = 'log' if xlog else 'linear'
	if yscale == None: 
		yscale = 'log' if ylog else 'linear'

	xr, yr =  set_range(xdata, ydata, xr=xr, yr=yr, 
			margin=margin, drawdown=drawdown,
			xscale=xscale, yscale=yscale)

	if filter:
		xdata, ydata = filter_by_range(xdata, ydata, xr, yr)

	if binsize != None:  binx,  biny = binsize, binsize
	if nbin    != None: nbinx, nbiny = nbin,    nbin

	if binx==None:  binx = (xr[1]-xr[0])/nbinx
	else:          nbinx = int((xr[1]-xr[0])/binx)

	if biny==None:  biny = (yr[1]-yr[0])/nbiny
	else:          nbiny = int((yr[1]-yr[0])/biny)

	xedges, yedges = nbinx, nbiny

	if xscale == 'log': xedges = get_log_edges(xr, nbinx)
	if yscale == 'log': yedges = get_log_edges(yr, nbiny)

	bins = [xedges, yedges]

	# to get zmax
	heatmap, *_ = np.histogram2d(xdata, ydata, bins=bins)
	zmax=np.max(heatmap.T)

	def show(ion=True):
		if ion: plt.ion()
		if not zlog:
			image, xedges, yedges, qmesh = plt.hist2d(xdata, ydata, bins=bins, cmap=cmap)
		else:
			# log, with negative
			zmin_= 0.5 if zmin == 0 else zmin

			image, xedges, yedges, qmesh = plt.hist2d(xdata, ydata, 
					norm=colors.LogNorm(vmin=zmin_, vmax=zmax),
					bins=bins,  cmap=cmap)
		plt.colorbar()

		wrap(plt, xr, yr, xlabel, ylabel, title=title,
				xscale=xscale, yscale=yscale, outfile=outfile, ion=ion, display=display)
		return image


	image = show(ion=False)
	
	if hold: embed()

	return image

# this works but
# it is too annoying to keep these variables
# so don't use this until finding a better way
def dplot_traffic(style='xydata'):
	def traffic(xdata, ydata, 
		data=None, infile=None, outfile=None, 
		x=None, y=None, 
		margin=None,
		xr=None, yr=None, filter=False, drawdown=None,
		xscale='linear', yscale='linear',
		xlabel=None, ylabel=None,
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, zmin=0,
		cmap='Blues', aspect='auto',
		interpolation=None,
		hold=True, hdu=1, ftype=None):
		print(style)
		if   style == 'xydata': 
			return dplot(xdata, ydata,
					data=data, infile=infile, outfile=outfile, 
					x=x, y=y, 
					margin=margin,
					xr=xr, yr=yr, filter=filter, drawdown=drawdown,
					xscale=xscale, yscale=yscale,
					xlabel=xlabel, ylabel=ylabel,
					binx=binx, biny=binx, nbinx=nbinx, nbiny=nbiny, nbin=nbin, binsize=binsize,
					zlog=zlog, zmin=zmin,
					cmap=cmap, aspect=aspect,
					interpolation=interpolation,
					hold=hold, hdu=hdu, ftype=ftype)
		elif style == 'file':   
			return dplot(None, None, 
					data=data, infile=infile, outfile=outfile, 
					x=x, y=y, 
					margin=margin,
					xr=xr, yr=yr, filter=filter, drawdown=drawdown,
					xscale=xscale, yscale=yscale,
					xlabel=xlabel, ylabel=ylabel,
					binx=binx, biny=binx, nbinx=nbinx, nbiny=nbiny, nbin=nbin, binsize=binsize,
					zlog=zlog, zmin=zmin,
					cmap=cmap, aspect=aspect,
					interpolation=interpolation,
					hold=hold, hdu=hdu, ftype=ftype)
	return traffic
