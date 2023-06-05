
This branch contains a solution to support 10% errors margins on statrting state AT THE COST OF FUEL.
It automatically runs all possible margins [1.0, 1.1, 0.9] on "vs", "alt", "hs", "fuel".

We treated the flight function as a function with multi variables and used scipy minimize function to find best values to satisfy conditions.
This solution also hovers vertically to cancel out any residual hs left when vertically landing.

You can disable/enable CSV and plotting by changing the vars: `need_csv` and `need_plot`

Dont forget:  
`pip install -r requirements.txt`

Typical output:
````
Running with params with error 1.0 on vs
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(11.930542576399887, 0.7474457607269205, 0.3424426484735923, 0.09580079389393814, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 1.0 on alt
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(11.930542576399887, 0.7474457607269205, 0.3424426484735923, 0.09580079389393814, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 1.0 on ang
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(11.930542576399887, 0.7474457607269205, 0.3424426484735923, 0.09580079389393814, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 1.0 on fuel
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(11.930542576399887, 0.7474457607269205, 0.3424426484735923, 0.09580079389393814, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 1.1 on vs
{'vs': 27.280000000000005, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(11.52597460322382, 0.4590628870936917, 0.3552157806143459, 0.2686088453326349, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 1.1 on alt
{'vs': 24.8, 'hs': 932.0, 'alt': 15122.800000000001, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(5.187921694808965, 0.7848928918926603, 0.34241712380058553, -0.01827516257792248, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 1.1 on ang
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 64.13, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(11.94728211113496, 0.7471207959400117, 0.3424683351322815, 0.08901395240938974, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 1.1 on fuel
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 133.10000000000002, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(20.089437839487015, 0.628650698798765, 0.3516130487350091, 0.14814620409959872, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 0.9 on vs
{'vs': 22.32, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(12.190064526689524, 0.48024568076965934, 0.3485754248374131, 0.1441187633689088, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 0.9 on alt
{'vs': 24.8, 'hs': 932.0, 'alt': 12373.2, 'ang': 58.3, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(18.939335019210407, 0.4883440639158887, 0.34585560987171426, -0.5159184521713508, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 0.9 on ang
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 52.47, 'fuel': 121.0, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(11.913817049018476, 0.7477907557653041, 0.3424140702592269, 0.10358528462963312, [25, 58.02236798, 77.47671845, 2000.0, 20])


Running with params with error 0.9 on fuel
{'vs': 24.8, 'hs': 932.0, 'alt': 13748.0, 'ang': 58.3, 'fuel': 108.9, 'need_csv': False, 'need_plot': False}
fuel_left, alt, vs, hs, flight_config
(3.808566019399765, 0.7906367525326126, 0.3459723230222702, 0.05262767178188497, [25, 58.02236798, 77.47671845, 2000.0, 20])
[25, 58.02236798, 77.47671845, 2000.0, 20]
````
