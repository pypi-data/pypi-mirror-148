""" Utility functions and classes for SRP

Context : SRP
Module  : Stats.py
Version : 1.0.0
Author  : Stefano Covino
Date    : 30/04/2022
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : Akaike (loglikelihood,npars)
            This function reports the Akaike information criterion knowking the best-fit Log Likelihoood,
            and the number of fit parameters.

Remarks :

History : (30/04/2022) First version.

"""




def Akaike(LLike,npars):
    return -2*LLike+2*npars


    
    