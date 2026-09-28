Tarnbeck Institute of Hydrology 

TIH/TN/18 

# **A one-dimensional model of tidal attenuation in the Braithe channel** 

Technical note TIH/TN/18  ·  January 2026 

_R. K. Sandiman and H. Vale_ 

## **1  Introduction** 

The tide entering the Braithe is attenuated over the eleven kilometres between the bar and Braithe Bridge, and the attenuation is large enough to matter to anyone predicting water levels in the upper estuary. This note sets out the one-dimensional model the Institute has used since 2018, states the approximation on which the working formula rests, and compares the result with the gauge record at three stations. 

Nothing here is new. The intention is to have the derivation, the assumptions and the coefficients in one place, because the formula has been quoted in Partnership papers without them. 

## **2  Governing equations** 

Take the channel as a single reach of slowly varying cross-section and neglect lateral inflow. Conservation of mass gives 



where _A_ is the cross-sectional area below the free surface and _Q_ the discharge through it. Conservation of momentum, with friction represented in the Manning form, gives 



in which _η_ is the surface elevation above mean sea level, _n_ is Manning's coefficient, _R_ the hydraulic radius _R_ = _A_ / _P_ for wetted perimeter _P_ , and _g_ the acceleration due to gravity. The friction term is the only nonlinear one that matters over the range of interest. 

## **3  Attenuation of the leading harmonic** 

For a channel of nearly uniform depth the leading semidiurnal harmonic decays close to exponentially with distance upstream, so that 



with _η_ 0 the amplitude at the bar, _ω_ the angular frequency of the harmonic, _k_ the wavenumber and _μ_ the attenuation coefficient. Linearising the friction term by the Lorentz method and collecting terms gives 

Page 1 of 3 

Tarnbeck Institute of Hydrology 

TIH/TN/18 



where _c_ is the frictionless wave speed and _h_ the mean depth. The second expression is the friction parameter; it is small in the lower reach and approaches unity above Harrowby Reach, which is where the exponential form begins to fail. 

## **4  Application to the Braithe** 

Taking the mean depth as eleven metres below the bar and four metres at the bridge, with Manning's coefficient at the value fitted in 2018, the formula reproduces the observed amplitude at Vardenne Quay to within four per cent and at Harrowby Reach to within nine. At Braithe Bridge it overestimates the amplitude, and the discrepancy grows through the spring tides, which is the behaviour the friction parameter predicts. 

A two-reach treatment with separate depths would probably remove most of the error at the bridge. It has not been attempted here because the gauge record above Harrowby Reach is too short to fit a second coefficient with any confidence. 

## **5  Coefficients** 

Manning's coefficient is not constant with depth in a channel of this kind, and the single fitted value used above is a compromise. Fitting the 2018 record with a depth-dependent form gives 



with _n_ ∞ the deep-water value and _b_ a bed constant. The fit is better in the lower reach and no better at the bridge, which suggests that the error there is not in the friction term at all. 

The two constants were fitted to the 2018 record and have not been refitted since. Refitting on the four years now available would be worth doing; the Institute's expectation is that the deep-water value will move very little and the bed constant appreciably, because it is carrying the shallow reaches where the record has improved most. 

## **6  Limitations** 

Three limitations should be stated plainly. The first is the one-dimensional assumption, which fails where the channel divides above Harrowby Reach. The second is the neglect of the freshwater inflow, which is small in summer and not small after rain. The third is the linearisation itself, which is a poor approximation once the friction parameter approaches unity - that is, in exactly the reach where the model is least accurate. 

The error measure quoted in the previous section is 

Page 2 of 3 

Tarnbeck Institute of Hydrology 

TIH/TN/18 

(6) 



_ηo_ 

taken over the spring-neap cycle at each gauge, with _ηo_ the observed amplitude and _ηm_ the modelled one. It is a crude measure and it flatters the model at the bar, where the amplitude is large and the absolute error is not. 

None of this is an argument against using the formula, which is quick, transparent and good enough for the purposes the Partnership puts it to. It is an argument for quoting it with the reach and the tidal range attached, which the papers that quote it have not always done. 

## **References** 

Sandiman, R. K. (2018). Tidal propagation in the Braithe: a first fit. Tarnbeck Institute internal report TIH/IR/09. Vale, H. and Croyde, P. (2021). The Harrowby Reach gauge, 2015 to 2020. Journal of Estuarine Hydrology 44, 218-31. 

Prosser, A. (2009). Friction coefficients for the Braithe channel. Braithe Harbour Board, unpublished. 

Page 3 of 3 

