Tool for nuclear calculations - in development

Examples:
=========

Kinematics
----------

Shoot deuteron at 24.4 MeV on c12 isotope, look at outgoing proton at 15
degrees that left the 13C excited at 3.089MeV (see appendix TUNL)

``` {.example}
./bin_nuphy2 kin -i h2,c12  -e 24.4  -o h1 -a 15 -x 3.089
```

Result:

``` {.example}
-- 15.0 deg  TKE=24.400 MeV Q= 2.722 MeV ------------
        th3cm=       16.74032
        th4cm=      163.25968
        th4  =       28.82888
        T3a  =       23.50155       T4b        0.00000
        T4a  =        3.62020       T4b       12.13499
        Kscsl=        0.80707 (sigma_cms=Kscsl*sigma_lab)
        rho3 =        0.11705 (if <=1.0 : 1 solution else 2 solutions for T3)
        p1   =      303.56252 (projectile momentum)
        V    =        0.02321 (velocity of CMS ... v/c)
        ttr  =        0.00000 (Threshold in Lab)
        ttrc =        0.00000 (Threshold in CMS == -Q)
        Q    =        2.72174 (if Q>0 = exoterm  [MeV])
        ExcT =        3.08900 (input tgt excitation)
        p3c  =      189.93230
        p4c  =      189.93230
 TKECMS(1,2) =       20.87655
EtotCMS(3,4) =       20.70207
        p3   =      211.37177     b  p3b  =      168.41384
        p4   =      296.20106     b  p4b  =      542.39606
        beta1=        0.15973    47.9mm/ns
        beta3=        0.21966    65.9mm/ns
        beta4=        0.02444    7.3mm/ns
   TKEout t3a =       23.50155
```

The last line *t3a* is Total Kinetic Energy of the outgoing h1 (particle
3).

There are few interesting things:

-   Theta 3 and 4 in CMS

<!-- -->

-   Total kinetic energy 3 and 4
    -   factor to translate sigma to CMS,
    -   Threshold in Lab and CMS
    -   Q of reaction

**Two kinematics example**

Scattering (elastic) of alpha particle on proton

``` {.example}
./bin_nuphy2 kin -i he4,h1  -e 24.4  -o h1 -a 15
```

``` {.example}
--- 15.0 deg  TKE=24.400 MeV Q= 0.000 MeV ------------
        th3cm=       40.27772
        th4cm=      139.72228
        th4  =        6.39349
        T3a  =        9.01720       T4b        0.67407
        T4a  =       15.38280       T4b       23.72593
        Kscsl=        0.14504 (sigma_cms=Kscsl*sigma_lab)
        rho3 =        1.63980 (if <=1.0 : 1 solution else 2 solutions for T3)
     b  th3cm=      169.84178
     b  th4cm=       10.15822
     b  th4  =        1.34279
     b  T3(b)=        0.67407
     b  T4(b)=       23.72593
     b Kscslb=        1.94886 sigma_cms=K*sigma_lab)
        p1   =      427.24856 (projectile momentum)
        V    =        0.09107 (velocity of CMS ... v/c)
        ttr  =        0.00000 (Threshold in Lab)
        ttrc =        0.00000 (Threshold in CMS == -Q)
        Q    =        0.00000 (if Q>0 = exoterm  [MeV])
        ExcT =        3.08900 (input tgt excitation)
        p3c  =       52.21631
        p4c  =       52.21631
 TKECMS(1,2) =        4.90537
EtotCMS(3,4) =        1.81751
        p3   =      130.42892     b  p3b  =       35.58175
        p4   =      339.17273     b  p4b  =      421.46065
        beta1=        0.11385    34.2mm/ns
        beta3=        0.13761    41.3mm/ns
        beta4=        0.09052    27.2mm/ns
        t3a  =        9.01720   and  t3b  0.674068  (TKE)
```

Two kinamatics are calculated (a and b)

Srim
----

Run 40MeV/A of 40Ar through mylar

``` {.example}
/bin_nuphy2 sri -i ar40 -m mylar -e 1600 -t 3um
```

Run the same beam through 12cm of isobutane at 950 mbar 20deg C

``` {.example}
./bin_nuphy2 sri -i ar40 -m hisobutane -e 1600 -t 120mm -p 95000 -k 293
```

Same through the layer of mylar+isobutane

``` {.example}
./bin_nuphy2 sri -i ar40 -m hisobutane -e 1600 -t 120mm -p 95000 -k 293
```

Similar, two mylar windows:

``` {.example}
./bin_nuphy2 sri -i ar40  -m mylar,hisobutane,mylar -e 1600 -t 3um,120mm,3um -p 95000 -k 293
```

Using directly a *srim.py* module form git repository and write an *h5*
file with results

``` {.example}
./srim.py -i h1 -m al -e 24.4 -t 3mm -n 300 -w a.h5
```

Some useful databases
=====================

-   TOI - <http://nucleardata.nuclear.lu.se/toi/nuclide.asp?iZA=260059>
-   DECAY - <https://www.nndc.bnl.gov/nudat2/indx_dec.jsp>
-   TUNL -
    <https://nucldata.tunl.duke.edu/nucldata/figures/13figs/menu13.shtml>

Progress
========

  ------------ ------- ------------ ------- -------- -------- -------------------------- --------------------
               In      FireWrks     Fully            In                                  
  module       Place   ParamCheck   Func    Pytest   BinDir   description1               description2
  prj~utils~   y       NO           NEVER   NO       NO       Color,Fail,Print,GetFile   
  isotope      y       y            \~      y        y        gives isotope data         used by kinematics
  kinematics   y       y            y       y        y        kinematic calc             
  rolfs        y       y            y       y                                            
  srim         y                                                                         
  xsections                                                                              
  yields                                                                                 
  radcap                                                                                 
  tendl                                                                                  
  fispact                                                     from nuphy1                
  sr                                                          nuphy1                     
  spectra                                                     nuphy1                     
  ------------ ------- ------------ ------- -------- -------- -------------------------- --------------------
