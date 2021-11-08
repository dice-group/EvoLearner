:- modeh(1,hepatitisb(+patient)).
:- modeb(1,patient(+patient)).
:- modeb(1,has_sex(+patient,-sex)).
:- modeb(1,has_biopsy(+patient,-biopsy)).
:- modeb(1,fibrosis_level(+biopsy,#int)).
:- modeb(1,activity_level(+biopsy,#int)).
:- modeb(1,screening(+screening)).
:- modeb(1,glutamic_oxaloacetic_transaminase_level(+screening,#int)).
:- modeb(1,glutamic_pyruvic_transaminase_level(+screening,#int)).
:- modeb(1,albumin_level(+screening,#int)).
:- modeb(1,total_bilirubin_level(+screening,#int)).
:- modeb(1,direct_bilirubin_level(+screening,#int)).
:- modeb(1,colisterase_activity_level(+screening,#int)).
:- modeb(1,thymol_turbidity_test_level(+screening,#int)).
:- modeb(1,zinc_sulfate_turbidity_test_level(+screening,#int)).
:- modeb(1,total_cholesterol_level(+screening,#int)).
:- modeb(1,total_protein_level(+screening,#int)).
:- modeb(1,has_screening(+patient,-screening)).
:- modeb(1,dur(+patient,#int)).

:- determination(hepatitisb/1,patient/1).
:- determination(hepatitisb/1,has_sex/2).
:- determination(hepatitisb/1,has_biopsy/2).
:- determination(hepatitisb/1,fibrosis_level/2).
:- determination(hepatitisb/1,activity_level/2).
:- determination(hepatitisb/1,screening/1).
:- determination(hepatitisb/1,glutamic_oxaloacetic_transaminase_level/2).
:- determination(hepatitisb/1,glutamic_pyruvic_transaminase_level/2).
:- determination(hepatitisb/1,albumin_level/2).
:- determination(hepatitisb/1,total_bilirubin_level/2).
:- determination(hepatitisb/1,direct_bilirubin_level/2).
:- determination(hepatitisb/1,colisterase_activity_level/2).
:- determination(hepatitisb/1,thymol_turbidity_test_level/2).
:- determination(hepatitisb/1,zinc_sulfate_turbidity_test_level/2).
:- determination(hepatitisb/1,total_cholesterol_level/2).
:- determination(hepatitisb/1,total_protein_level/2).
:- determination(hepatitisb/1,has_screening/2).
:- determination(hepatitisb/1,dur/2).
