# This is binned Poisson fitting for muon data
# 4 spacebar!!!!!!!!!!!!!!
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ROOT import *
from scipy.optimize import curve_fit
from scipy.special import factorial
from scipy.stats import poisson
import os
import math

# read csv file
df = pd.read_csv('CSMHUNT_12300_2022-2-21_3-14-58_2월.csv', sep=';')
drop_idx = df.loc[ df[' coinc ']!=' ABC'].index
df = df.drop(drop_idx)
df = df.drop([0,1], axis=0)
counts = df[' COINC ']

# fill histogram
h = TH1F('Detected Muon Multiplicity', 'Poisson Distribution of Cosmic Rays', 60, 200, 800)
for i in counts:
	h.Fill(i)

h.SetXTitle("Detected counts per 600 sec")
h.SetYTitle("Entreis")
h.SetMaximum( float( h.GetMaximum() ) * 1.1 )
h.SetFillColor(kBlue-10)
h.SetLineColor(kBlue)
h.GetXaxis().SetTitleSize(0.04)
h.GetYaxis().SetTitleSize(0.04)

c = TCanvas('c', 'c', 3)
c.SetLeftMargin(0.15)

# poisson fit
f = TF1("f", "[0] *TMath::Poisson((x/[2]), ([1]/[2]))", h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
f.SetParameters(h.GetBinContent(h.GetMaximumBin()) / 0.15, h.GetMean(), h.GetMean()/5)
f.SetParNames("Constant", "Mean", "XScaling")
f.SetNpx(1000)

gStyle.SetTitleFontSize(0.045)
gStyle.SetOptStat("e")
gStyle.SetOptFit(112)
gStyle.SetStatBorderSize(0)
gStyle.SetStatFontSize(0.03)
gStyle.SetStatX(0.89)
gStyle.SetStatY(0.89)
gStyle.SetStatW(0.2)
gStyle.SetStatH(0.16)
gStyle.SetTitleY(0.97)

h.Fit(f,"")


#c.Print(Form("Poisson_%s.pdf"%tag))
c.Print(Form("Poisson_Feb.pdf"))
