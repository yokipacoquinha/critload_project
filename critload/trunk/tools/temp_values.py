# ******************************************************
## Revision "$LastChangedDate: 2019-03-14 08:53:42 +0100 (Thu, 14 Mar 2019) $"
## Date "$LastChangedRevision: 625 $"
## Author "$LastChangedBy: arthurbeusen $"
## URL "$HeadURL: http://pbl.sliksvn.com/globalnutrients/critload/trunk/tools/temp_values.py $"
## Copyright 2019, PBL Netherlands Environmental Assessment Agency and Wageningen University.
## Reuse permitted under Gnu Public License, GPL v3.
# ******************************************************

# Python modules
import os

# Generalcode modules
import ascraster

# Local modules
from print_debug import *

def griddivide(grid1,grid2,default_nodata_value = 0):
    '''
    Calculate result of grid1/grid2 
    '''
    # Make a copy of the first grid.
    grid3 = ascraster.duplicategrid(grid1)

    for icell in range(grid3.length):
        # Get values from both grids.
        val1 = grid1.get_data(icell)
        val2 = grid2.get_data(icell)

        # If both grids have nodata, keep nodata.
        if (val1 == None or val2 == None):
            continue
        # Do the calculation
        try:
            val3 = val1/val2
        except (ZeroDivisionError,TypeError):
            val3 = default_nodata_value
        
        # Put result in grid.
        grid3.set_data(icell,val3)

    return grid3
    
def temp_values(params):
    
    ### --------- 1. LAND UNSE FRACTIONS --------- ###
    # read input files land areas
    a_tot = ascraster.Asciigrid(ascii_file=params.filename_gridcell_area, numtype=float,mask=params.mask)
    a_ag  = ascraster.Asciigrid(ascii_file=params.filename_agri_area,     numtype=float,mask=params.mask)
    a_ara = ascraster.Asciigrid(ascii_file=params.filename_cropland_area, numtype=float,mask=params.mask)  
    a_igl = ascraster.Asciigrid(ascii_file=params.filename_intgl_area,    numtype=float,mask=params.mask)     
    a_egl = ascraster.Asciigrid(ascii_file=params.filename_extgl_area,    numtype=float,mask=params.mask)
    a_nat = ascraster.Asciigrid(ascii_file=params.filename_natural_area,  numtype=float,mask=params.mask)
    
    # calculate fag   
    fag = ascraster.duplicategrid(a_ag)
    fag.divide(a_tot, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"fag.asc")
    #fag.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fag,"fag =")
    # calculate fara
    fara = ascraster.duplicategrid(a_ara)
    fara.divide(a_tot, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"fara.asc")
    #fara.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fara,"fara =")   
    # calculate figl
    figl = ascraster.duplicategrid(a_igl)
    figl.divide(a_tot, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"figl.asc")
    #figl.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(figl,"figl =")   
    # calculate fagri
    fagri = ascraster.duplicategrid(a_ara)
    fagri.add(a_igl)
    fagri.divide(a_tot, default_nodata_value = -9999)
    fileout = os.path.join(params.outputdir,"fagri.asc")
    fagri.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fagri,"fagri =")   
    # calculate fegl
    fegl = ascraster.duplicategrid(a_egl)
    fegl.divide(a_tot, default_nodata_value = -9999)
    fileout = os.path.join(params.outputdir,"fegl.asc")
    fegl.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fegl,"fegl =")   
    # calculate fnat
    fnat = ascraster.duplicategrid(a_nat)
    fnat.divide(a_tot, default_nodata_value = -9999)
    fileout = os.path.join(params.outputdir,"fnat.asc")
    fnat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fnat,"fnat =")
    # calculate fland
    fland = ascraster.duplicategrid(a_ag)
    fland.add(a_nat)
    fland.divide(a_tot, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"fland.asc")
    #fland.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fland,"fland =")
  
    ### --------- 2. INPUTS FERTILIZER, MANURE, FIXATION --------- ###
    # read input files N inputs 
    n_fert_ag   = ascraster.Asciigrid(ascii_file=params.filename_fert_inp,            numtype=float,mask=params.mask)
    n_fert_ara  = ascraster.Asciigrid(ascii_file=params.filename_fert_inp_cropland,   numtype=float,mask=params.mask)
    n_fert_igl  = ascraster.Asciigrid(ascii_file=params.filename_fert_inp_grassland,  numtype=float,mask=params.mask)  
    n_man_ag    = ascraster.Asciigrid(ascii_file=params.filename_manure_inp,          numtype=float,mask=params.mask)    
    n_man_ara   = ascraster.Asciigrid(ascii_file=params.filename_manure_inp_cropland, numtype=float,mask=params.mask)
    n_man_igl   = ascraster.Asciigrid(ascii_file=params.filename_manure_inp_intgl,    numtype=float,mask=params.mask)    
    n_man_egl   = ascraster.Asciigrid(ascii_file=params.filename_manure_inp_extgl,    numtype=float,mask=params.mask)  
    n_fix_ag    = ascraster.Asciigrid(ascii_file=params.filename_nfixation_agri,      numtype=float,mask=params.mask)
    n_fix_ara   = ascraster.Asciigrid(ascii_file=params.filename_nfixation_cropland,  numtype=float,mask=params.mask)
    n_fix_igl   = ascraster.Asciigrid(ascii_file=params.filename_nfixation_intgl,     numtype=float,mask=params.mask)
    n_fix_egl   = ascraster.Asciigrid(ascii_file=params.filename_nfixation_extgl,     numtype=float,mask=params.mask)

    # Calculate N inputs to 'agri' - fertilizer
    n_fert_agri = ascraster.duplicategrid(n_fert_ara)
    n_fert_agri.add(n_fert_igl)
    #fileout = os.path.join(params.outputdir,"n_fert_agri.asc")
    #n_fert_agri.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_fert_agri,"n_fert_agri =")
    # Calculate N inputs to 'agri' - manure
    n_man_agri = ascraster.duplicategrid(n_man_ara)
    n_man_agri.add(n_man_igl)
    #fileout = os.path.join(params.outputdir,"n_man_agri.asc")
    #n_man_agri.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_man_agri,"n_man_agri =")
    # Calculate N inputs to 'agri' - N fixation
    n_fix_agri = ascraster.duplicategrid(n_fix_ara)
    n_fix_agri.add(n_fix_igl)
    fileout = os.path.join(params.outputdir,"n_fix_agri.asc")
    n_fix_agri.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_fix_agri,"n_fix_agri =")
    
    # calculate frNfe_ag
    fert_man_ag = ascraster.duplicategrid(n_man_ag)
    fert_man_ag.add(n_fert_ag)
    frnfe_ag = griddivide(n_fert_ag,fert_man_ag,default_nodata_value = 0)
    
    # replace '0' by 0.0001 in frNfe_ag
    for icell in range(frnfe_ag.length):
        val = frnfe_ag.get_data(icell)
        if (val == None or val > 0):
            continue
        if val == 0.0:
            res = 0.0001
        frnfe_ag.set_data(icell,res) 
    
    # replace '1' by 0.9999 in frNfe_ag
    for icell in range(frnfe_ag.length):
        val = frnfe_ag.get_data(icell)
        if (val == None or val < 1):
            continue
        if val == 1.0:
            res = 0.9999
        frnfe_ag.set_data(icell,res) 
    
    print_debug(frnfe_ag,"frNfe_ag =")
    #fileout = os.path.join(params.outputdir,"frnfe_ag.asc")
    #frnfe_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)

    ####CHECK: INDEED OK TO GET NA VALUES FOR DIV ZERO WITH frNfe?
    # calculate frNfe_agri
    fert_man_agri = ascraster.duplicategrid(n_fert_agri)
    fert_man_agri.add(n_man_agri)
    fileout = os.path.join(params.outputdir,"fert_man_agri.asc")
    fert_man_agri.write_ascii_file(fileout, output_nodata_value=-9999,compress=params.lcompress)    
    
    
    frnfe_agri = ascraster.duplicategrid(n_fert_agri)
    frnfe_agri.divide(fert_man_agri)
    #frnfe_agri = griddivide(n_fert_agri,fert_man_agri,default_nodata_value = 0)
    
    # replace '0' by 0.0001 in frNfe_agri
    for icell in range(frnfe_agri.length):
        val = frnfe_agri.get_data(icell)
        if (val == None or val > 0):
            continue
        if val == 0.0:
            res = 0.0001
        frnfe_agri.set_data(icell,res) 
    
    # replace '1' by 0.9999 in frnfe_agri
    for icell in range(frnfe_agri.length):
        val = frnfe_agri.get_data(icell)
        if (val == None or val < 1):
            continue
        if val == 1.0:
            res = 0.9999
        frnfe_agri.set_data(icell,res) 
    
    print_debug(frnfe_agri,"frnfe_agri =")
    fileout = os.path.join(params.outputdir,"frnfe_agri.asc")
    frnfe_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
   
   
    ### --------- 3. NH3 EMISSIONS & EMISSION FRACTIONS --------- ###
    # read input files NH3 emissions
    nh3_spread_man      = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_manure,          numtype=float,mask=params.mask)
    nh3_spread_man_ara  = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_manure_cropland, numtype=float,mask=params.mask)
    nh3_spread_man_igl  = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_manure_intgl,    numtype=float,mask=params.mask)
    nh3_spread_man_egl  = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_manure_extgl,    numtype=float,mask=params.mask)
    nh3_stor            = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_storage,                numtype=float,mask=params.mask)
    nh3_graz            = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_grazing,                numtype=float,mask=params.mask)
    nh3_graz_igl        = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_grazing_int,            numtype=float,mask=params.mask)
    nh3_graz_egl        = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_grazing_ext,            numtype=float,mask=params.mask)
    nh3_spread_fert     = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_fert,            numtype=float,mask=params.mask)    
    nh3_spread_fert_ara = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_fert_cropland,   numtype=float,mask=params.mask)
    nh3_spread_fert_igl = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_fert_intgl,      numtype=float,mask=params.mask)    
    nh3_spread_fert_egl = ascraster.Asciigrid(ascii_file=params.filename_nh3_em_spread_fert_extgl,      numtype=float,mask=params.mask)
    
    # calculate total NH3 emission (all agriculture)
    nh3_tot = ascraster.duplicategrid(nh3_spread_man)
    nh3_tot.add(nh3_stor)
    nh3_tot.add(nh3_graz)
    nh3_tot.add(nh3_spread_fert)
    print_debug(nh3_tot,"nh3_tot =")

    # calculate total NH3 emission (ara + igl)
    nh3_spread_fert_agri = ascraster.duplicategrid(nh3_spread_fert_ara)
    nh3_spread_fert_agri.add(nh3_spread_fert_igl)
    nh3_tot_agri = ascraster.duplicategrid(nh3_spread_fert_agri)
    nh3_tot_agri.add(nh3_spread_man_ara)
    nh3_tot_agri.add(nh3_spread_man_igl)
    nh3_tot_agri.add(nh3_stor)
    nh3_tot_agri.add(nh3_graz_igl)
    print_debug(nh3_tot_agri,"nh3_tot_agri =")

    # calculate total NH3 emission (egl)
    nh3_tot_egl = ascraster.duplicategrid(nh3_spread_man_egl)
    nh3_tot_egl.add(nh3_graz_egl)
    nh3_tot_egl.add(nh3_spread_fert_egl)
    fileout = os.path.join(params.outputdir,"nh3_tot_egl.asc")
    nh3_tot_egl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)   
    print_debug(nh3_tot_egl,"nh3_tot_egl =")    
    
    # calculate fnh3em,man
    nh3_man_tot = ascraster.duplicategrid(nh3_tot)
    nh3_man_tot.substract(nh3_spread_fert)
    nh3_ef_man = griddivide(nh3_man_tot,n_man_ag,default_nodata_value = 0)
    #fileout = os.path.join(params.outputdir,"nh3_ef_man.asc")
    #nh3_ef_man.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nh3_ef_man,"nh3_ef_man =")
    
    # calculate fnh3em,man,agri
    nh3_man_tot_agri = ascraster.duplicategrid(nh3_tot_agri)
    nh3_man_tot_agri.substract(nh3_spread_fert_agri)
    nh3_ef_man_agri = griddivide(nh3_man_tot_agri,n_man_agri,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"nh3_ef_man_agri.asc")
    nh3_ef_man_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nh3_ef_man_agri,"nh3_ef_man_agri =")
    
    # calculate fnh3em,fert
    nh3_ef_fert = griddivide(nh3_spread_fert,n_fert_ag,default_nodata_value = 0)
    #fileout = os.path.join(params.outputdir,"nh3_ef_fert.asc")
    #nh3_ef_fert.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nh3_ef_fert,"nh3_ef_fert =")

    # calculate fnh3em,fert,agri
    nh3_ef_fert_agri = griddivide(nh3_spread_fert_agri,n_fert_agri,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"nh3_ef_fert_agri.asc")
    nh3_ef_fert_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nh3_ef_fert_agri,"nh3_ef_fert_agri =")
    
    ### --------- 4. N DEPOSITION & NOx emission --------- ###
    # calculate corrected N deposition grid - for all cells where Ndep < NH3em, replace Ndep by NH3em
    ndep_tot = ascraster.Asciigrid(ascii_file=params.filename_n_deposition,numtype=float,mask=params.mask)
    ndep_tot_corr = ascraster.duplicategrid(ndep_tot)
    for icell in range(nh3_tot.length):
        # Get values from both grids.
        nh3 =  nh3_tot.get_data(icell)
        dep = ndep_tot.get_data(icell)
    
        # If both grids have nodata, keep nodata.
        if (nh3 == None or dep == None or dep >= nh3):
            continue
        if dep < nh3:
            depcorr = nh3
        ndep_tot_corr.set_data(icell,depcorr)
    #fileout = os.path.join(params.outputdir,"ndep_tot_corr.asc")
    #ndep_tot_corr.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)    
    print_debug(ndep_tot,"ndep_tot =")
    print_debug(ndep_tot_corr,"ndep_tot_corr =")
  
    # calculate NOx emissions: NOx = *corrected* Ndep - (NH3,spread,fe+NH3,spread,man+NH3stor+NH3,graz)
    nox_em = ascraster.duplicategrid(ndep_tot_corr)
    nox_em.substract(nh3_tot)
    fileout = os.path.join(params.outputdir,"nox_em.asc")
    nox_em.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nox_em,"nox_em =") 
 
    # calculate ndep_ag
    ndep_ag = ascraster.duplicategrid(ndep_tot_corr)
    ndep_ag.multiply(fag)
    #fileout = os.path.join(params.outputdir,"ndep_ag.asc")
    #ndep_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ndep_ag,"ndep_ag =")
    # calculate ndep_ara
    ndep_ara = ascraster.duplicategrid(ndep_tot_corr)
    ndep_ara.multiply(fara)
    #fileout = os.path.join(params.outputdir,"ndep_ara.asc")
    #ndep_ara.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ndep_ara,"ndep_ara =")
    # calculate ndep_igl
    ndep_igl = ascraster.duplicategrid(ndep_tot_corr)
    ndep_igl.multiply(figl)
    #fileout = os.path.join(params.outputdir,"ndep_igl.asc")
    #ndep_igl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ndep_igl,"ndep_igl =") 
    # calculate ndep_agri
    ndep_agri = ascraster.duplicategrid(ndep_tot_corr)
    ndep_agri.multiply(fagri)
    #fileout = os.path.join(params.outputdir,"ndep_agri.asc")
    #ndep_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ndep_agri,"ndep_agri =")
    # calculate ndep_egl
    ndep_egl = ascraster.duplicategrid(ndep_tot_corr)
    ndep_egl.multiply(fegl)
    #fileout = os.path.join(params.outputdir,"ndep_egl.asc")
    #ndep_egl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ndep_egl,"ndep_egl =")    
   
    ### --------- 5. TOTAL INPUTS --------- ###
    # calculate n_in_ag
    n_in_ag = ascraster.duplicategrid(n_fert_ag)
    n_in_ag.add(n_man_ag)
    n_in_ag.add(n_fix_ag)
    n_in_ag.add(ndep_ag)
    #fileout = os.path.join(params.outputdir,"n_in_ag.asc")
    #n_in_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_in_ag,"n_in_ag =")
    # calculate n_in_ara
    n_in_ara = ascraster.duplicategrid(n_fert_ara)
    n_in_ara.add(n_man_ara)
    n_in_ara.add(n_fix_ara)
    n_in_ara.add(ndep_ara)
    #fileout = os.path.join(params.outputdir,"n_in_ara.asc")
    #n_in_ara.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_in_ara,"n_in_ara =")    
    # calculate n_in_igl
    n_in_igl = ascraster.duplicategrid(n_fert_igl)
    n_in_igl.add(n_man_igl)
    n_in_igl.add(n_fix_igl)
    n_in_igl.add(ndep_igl)
    #fileout = os.path.join(params.outputdir,"n_in_igl.asc")
    #n_in_igl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_in_igl,"n_in_igl =")    
    # calculate n_in_agri    
    n_in_agri = ascraster.duplicategrid(n_in_ara)
    n_in_agri.add(n_in_igl)
    #fileout = os.path.join(params.outputdir,"n_in_agri.asc")
    #n_in_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_in_agri,"n_in_agri =")        
    # calculate n_in_egl
    n_in_egl = ascraster.duplicategrid(n_man_egl)
    n_in_egl.add(n_fix_egl)
    n_in_egl.add(ndep_egl)
    #fileout = os.path.join(params.outputdir,"n_in_egl.asc")
    #n_in_egl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_in_egl,"n_in_egl =")    
 
    ### --------- 6. SURFACE RUNOFF, UPTAKE, FRNUP, NUE --------- ###
    # read input files uptake, surface runoff
    nsro_ag  = ascraster.Asciigrid(ascii_file=params.filename_nsro_ag,         numtype=float,mask=params.mask)    
    n_up_ara = ascraster.Asciigrid(ascii_file=params.filename_uptake_cropland, numtype=float,mask=params.mask)
    n_up_igl = ascraster.Asciigrid(ascii_file=params.filename_uptake_intgl,    numtype=float,mask=params.mask)   
    n_up_egl = ascraster.Asciigrid(ascii_file=params.filename_uptake_extgl,    numtype=float,mask=params.mask)   
    
    
    #$# To manipulate results for 1999 so that I can also get uptake per land-use type (assuming equal NUE)
    #$#n_up_ag = ascraster.Asciigrid(ascii_file=params.filename_uptake_agriculture,    numtype=float,mask=params.mask)  #$#
    
    #$#nue_ag = ascraster.duplicategrid(n_up_ag)
    #$#nue_ag.divide(n_in_ag, default_nodata_value = -9999)
    
    #$#n_up_ara = ascraster.duplicategrid(n_in_ara)
    #$#n_up_ara.multiply(nue_ag)
    #$#fileout = os.path.join(params.inputdir,"n_up_crops.asc")
    #$#n_up_ara.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)   
    
    #$#n_up_igl = ascraster.duplicategrid(n_in_igl)
    #$#n_up_igl.multiply(nue_ag)
    #$#fileout = os.path.join(params.inputdir,"n_up_grass_int.asc")
    #$#n_up_igl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)   
    
    #$#n_up_egl = ascraster.duplicategrid(n_in_egl)
    #$#n_up_egl.multiply(nue_ag)
    #$#fileout = os.path.join(params.inputdir,"n_up_grass_ext.asc")
    #$#n_up_egl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)   

    
    # calculate uptake,agri
    n_up_agri = ascraster.duplicategrid(n_up_ara)
    n_up_agri.add(n_up_igl)
    #fileout = os.path.join(params.outputdir,"n_up_agri.asc")
    #n_up_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_up_agri,"n_up_agri =")     
    
    # calculate uptake,ag
    n_up_ag = ascraster.duplicategrid(n_up_agri)
    n_up_ag.add(n_up_egl)
    #fileout = os.path.join(params.outputdir,"n_up_ag.asc")
    #n_up_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(n_up_ag,"n_up_ag =")  
    
    # calculate runoff fraction fsro,ag
    fsro_ag = griddivide(nsro_ag,n_in_ag,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"fsro_ag.asc")
    fsro_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fsro_ag,"fsro_ag =") 
    
    # calculate nsro,agri
    nsro_agri = ascraster.duplicategrid(fsro_ag)
    nsro_agri.multiply(n_in_agri)
    #fileout = os.path.join(params.outputdir,"nsro_agri.asc")
    #nsro_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nsro_agri,"nsro_agri =")   
    
    # calculate frnup_agri
    n_in_min_nsro_agri = ascraster.duplicategrid(n_in_agri)
    n_in_min_nsro_agri.substract(nsro_agri)
    frnup_agri = griddivide(n_up_agri,n_in_min_nsro_agri,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"frnup_agri.asc")
    frnup_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(frnup_agri,"frnup_agri =")   
    
    # calculate nue_ara
    nue_ara = ascraster.duplicategrid(n_up_ara)
    nue_ara.divide(n_in_ara, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"nue_ara.asc")
    #nue_ara.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nue_ara,"nue_ara =")
    # calculate nue_igl
    nue_igl = ascraster.duplicategrid(n_up_igl)
    nue_igl.divide(n_in_igl, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"nue_igl.asc")
    #nue_igl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nue_igl,"nue_igl =")
    # calculate nue_agri
    nue_agri = ascraster.duplicategrid(n_up_agri)
    nue_agri.divide(n_in_agri, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"nue_agri.asc")
    #nue_agri.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nue_agri,"nue_agri =")
    # calculate nue_egl
    nue_egl = ascraster.duplicategrid(n_up_igl)
    nue_egl.divide(n_in_igl, default_nodata_value = -9999)
    #fileout = os.path.join(params.outputdir,"nue_egl.asc")
    #nue_egl.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nue_egl,"nue_egl =")    
       
    ### --------- 7. BUDGET, LEACHING, DENITRIFICATION --------- ###    
    # read input files
    ngw_ag = ascraster.Asciigrid(ascii_file=params.filename_groundwaterload_ag,numtype=float,mask=params.mask)
    fgw_rec_ag = ascraster.Asciigrid(ascii_file=params.filename_fraction_recent_groundwaterload_ag,numtype=float,mask=params.mask)
    nle_ag = ascraster.Asciigrid(ascii_file=params.filename_leaching_ag,numtype=float,mask=params.mask)
    
    # calculate N budget agriculture: Nbud,ag = Nin,ag - Nup,ag
    nbud_ag = ascraster.duplicategrid(n_in_ag)
    nbud_ag.substract(n_up_ag)
    fileout = os.path.join(params.outputdir,"nbud_ag.asc")
    nbud_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nbud_ag,"nbud_ag =")
    
    # calculate N load to surface water via groundwater due to *recent* N inputs: agriculture
    ngw_ag_rec = ascraster.duplicategrid(ngw_ag)
    ngw_ag_rec.multiply(fgw_rec_ag)
    fileout = os.path.join(params.outputdir,"ngw_ag_rec.asc")
    ngw_ag_rec.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ngw_ag_rec,"ngw_ag_rec =")
    
    # calculate Denitrification in soil: Nde,ag = Nbud,ag - Nsro,ag - Nle,ag
    nde_ag = ascraster.duplicategrid(nbud_ag)
    nde_ag.substract(nsro_ag)
    nde_ag.substract(nle_ag)
    fileout = os.path.join(params.outputdir,"nde_ag.asc")
    nde_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nde_ag,"nde_ag =")
        
    # calculate leaching fraction fle,ag
    nbud_min_nsro_ag = ascraster.duplicategrid(nbud_ag)
    nbud_min_nsro_ag.substract(nsro_ag)
    fle_ag = griddivide(nle_ag,nbud_min_nsro_ag,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"fle_ag.asc")
    fle_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fle_ag,"fle_ag =")     
    
    # calculate fraction of N leaching that is delivered to surface water via groundwater in first x years
    fgw_rec_le_ag = griddivide(ngw_ag_rec,nle_ag,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"fgw_rec_le_ag.asc")
    fgw_rec_le_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fgw_rec_le_ag,"fgw_rec_le_ag =")
    
    # calculate ndep_nat
    ndep_nat = ascraster.duplicategrid(ndep_tot_corr)
    ndep_nat.multiply(fnat)
    #fileout = os.path.join(params.outputdir,"ndep_nat.asc")
    #ndep_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ndep_nat,"ndep_nat =")

    # calculate N budget nature: Nbud,nat = Ndep,nat + Nfix,nat
    n_fix_nat = ascraster.Asciigrid(ascii_file=params.filename_nfixation_nat,numtype=float,mask=params.mask)
    nbud_nat = ascraster.duplicategrid(ndep_nat)
    nbud_nat.add(n_fix_nat)
    fileout = os.path.join(params.outputdir,"nbud_nat.asc")
    nbud_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nbud_nat,"nbud_nat =")
    
    # calculate N load to surface water via groundwater due to *recent* N inputs: natural areas
    ngw_nat = ascraster.Asciigrid(ascii_file=params.filename_groundwaterload_nat,numtype=float,mask=params.mask)
    fgw_rec_nat = ascraster.Asciigrid(ascii_file=params.filename_fraction_recent_groundwaterload_nat,numtype=float,mask=params.mask)
    ngw_nat_rec = ascraster.duplicategrid(ngw_nat)
    ngw_nat_rec.multiply(fgw_rec_nat)
    fileout = os.path.join(params.outputdir,"ngw_nat_rec.asc")
    ngw_nat_rec.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(ngw_nat_rec,"ngw_nat_rec =")
    
    # calculate Denitrification in soil: Nde,nat = Nbud,nat - Nsro,nat - Nle,nat
    nsro_nat = ascraster.Asciigrid(ascii_file=params.filename_nsro_nat,numtype=float,mask=params.mask)
    nle_nat = ascraster.Asciigrid(ascii_file=params.filename_leaching_nat,numtype=float,mask=params.mask)
    nde_nat = ascraster.duplicategrid(nbud_nat)
    nde_nat.substract(nsro_nat)
    nde_nat.substract(nle_nat)
    fileout = os.path.join(params.outputdir,"nde_nat.asc")
    nde_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nde_nat,"nde_nat =")
        
    # calculate leaching fraction fle,nat
    nbud_min_nsro_nat = ascraster.duplicategrid(nbud_nat)
    nbud_min_nsro_nat.substract(nsro_nat)
    fle_nat = griddivide(nle_nat,nbud_min_nsro_nat,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"fle_nat.asc")
    fle_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fle_nat,"fle_nat =")   
    
    # calculate runoff fraction fsro,nat
    fsro_nat = griddivide(nsro_nat,nbud_nat,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"fsro_nat.asc")
    fsro_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fsro_nat,"fsro_nat =")   
    
    # calculate fraction of N leaching that is delivered to surface water via groundwater in first x years - natural areas
    fgw_rec_le_nat = griddivide(ngw_nat_rec,nle_nat,default_nodata_value = 0)
    fileout = os.path.join(params.outputdir,"fgw_rec_le_nat.asc")
    fgw_rec_le_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(fgw_rec_le_nat,"fgw_rec_le_nat =")
    
    # calculate variable load to surface water from agriculture: Nload,var,ag = Nsro,ag + Ngw,rec,ag
    nload_var_ag = ascraster.duplicategrid(ngw_ag_rec)
    nload_var_ag.add(nsro_ag)
    #fileout = os.path.join(params.outputdir,"nload_var_ag.asc")
    #nload_var_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nload_var_ag,"nload_var_ag =")
    
    # calculate variable load to surface water from nature: Nload,var,nat = Nsro,nat + Ngw,rec,nat
    nload_var_nat = ascraster.duplicategrid(ngw_nat_rec)
    nload_var_nat.add(nsro_nat)
    #fileout = os.path.join(params.outputdir,"nload_var_nat.asc")
    #nload_var_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nload_var_nat,"nload_var_nat =")   

    # calculate fixed load to surface water from agriculture: Ngw,fixed,ag = Ngw,ag * (1-fgw,rec,ag)
    grid1 = ascraster.duplicategrid(fgw_rec_ag)
    for i in range(grid1.length):
        grid1.set_data(i,1.0)
    grid1.substract(fgw_rec_ag)
    nload_fixed_ag = ascraster.duplicategrid(ngw_ag)
    nload_fixed_ag.multiply(grid1)
    fileout = os.path.join(params.outputdir,"nload_fixed_ag.asc")
    nload_fixed_ag.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nload_fixed_ag,"nload_fixed_ag =")   
    
    # calculate fixed load to surface water from nature: Ngw,fixed,nat = Ngw,nat * (1-fgw,rec,nat)
    grid2 = ascraster.duplicategrid(fgw_rec_nat)
    for i in range(grid2.length):
        grid2.set_data(i,1.0)
    grid2.substract(fgw_rec_nat)
    nload_fixed_nat = ascraster.duplicategrid(ngw_nat)
    nload_fixed_nat.multiply(grid2)
    fileout = os.path.join(params.outputdir,"nload_fixed_nat.asc")
    nload_fixed_nat.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nload_fixed_nat,"nload_fixed_nat =")    

    # calculate total load from point sources
    nallo = ascraster.Asciigrid(ascii_file=params.filename_n_point_alloch_matter,numtype=float,mask=params.mask)
    nww = ascraster.Asciigrid(ascii_file=params.filename_n_point_wastewater,numtype=float,mask=params.mask)
    naqua = ascraster.Asciigrid(ascii_file=params.filename_n_point_aquaculture,numtype=float,mask=params.mask)
    ndep_sw = ascraster.Asciigrid(ascii_file=params.filename_n_point_dep_surfacewater,numtype=float,mask=params.mask)
    npoint_tot = ascraster.duplicategrid(nallo)
    npoint_tot.add(nww)
    npoint_tot.add(naqua)
    npoint_tot.add(ndep_sw)
    fileout = os.path.join(params.outputdir,"npoint_tot.asc")
    npoint_tot.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(npoint_tot,"npoint_tot =") 
    
    # calculate total load from erosion
    nero_ag = ascraster.Asciigrid(ascii_file=params.filename_n_in_erosion_ag,numtype=float,mask=params.mask)
    nero_nat = ascraster.Asciigrid(ascii_file=params.filename_n_in_erosion_nat,numtype=float,mask=params.mask)
    nero_tot = ascraster.duplicategrid(nero_ag)
    nero_tot.add(nero_nat)
    fileout = os.path.join(params.outputdir,"nero_tot.asc")
    nero_tot.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nero_tot,"nero_tot =")    
    
    # calculate total n load to surface water: Nload,tot = Nload,var,ag + Nload,var,nat + Ngw,fixed,ag + Ngw,fixed,nat + Npoint + Nero
    nload_tot = ascraster.duplicategrid(nload_var_ag)
    nload_tot.add(nload_var_nat)
    nload_tot.add(nload_fixed_ag)
    nload_tot.add(nload_fixed_nat)
    nload_tot.add(npoint_tot)
    nload_tot.add(nero_tot)
    #fileout = os.path.join(params.outputdir,"nload_tot.asc")
    #nload_tot.write_ascii_file(fileout,output_nodata_value=-9999,compress=params.lcompress)
    print_debug(nload_tot,"nload_tot =")        
    
