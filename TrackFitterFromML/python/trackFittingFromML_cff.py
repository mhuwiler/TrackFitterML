
import FWCore.ParameterSet.Config as cms

#fragment = cms.ProcessFragment( "TrackFittingFromML" )
# import propagator cff 


propagator = cms.ESProducer("PropagatorWithMaterialESProducer", # taken from https://github.com/cms-sw/cmssw/blob/6d2f66057131baacc2fcbdd203588c41c885b42c/TrackingTools/MaterialEffects/python/MaterialPropagator_cfi.py
    SimpleMagneticField = cms.string(""),
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('PropagatorWithMaterial'),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('alongMomentum'),
    useRungeKutta = cms.bool(False),
# If ptMin > 0, uncertainty in reconstructed momentum will be taken into account when estimating rms scattering angle.
# (By default, it is neglected). However, it will also be assumed that the track pt can't be below specified value,
# to prevent this scattering angle becoming too big.                                    
    ptMin = cms.double(-1.)
)

oppositePropagator = cms.ESProducer("PropagatorWithMaterialESProducer", # taken from https://github.com/cms-sw/cmssw/blob/6d2f66057131baacc2fcbdd203588c41c885b42c/TrackingTools/MaterialEffects/python/OppositeMaterialPropagator_cfi.py
    SimpleMagneticField = cms.string(""),
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('PropagatorWithMaterialOpposite'),
    Mass = cms.double(0.105),
    PropagationDirection = cms.string('oppositeToMomentum'),
    useRungeKutta = cms.bool(False),
# If ptMin > 0, uncertainty in reconstructed momentum will be taken into account when estimating rms scattering angle.
# (By default, it is neglected). However, it will also be assumed that the track pt can't be below specified value,
# to prevent this scattering angle becoming too big.                                    
    ptMin = cms.double(-1.)
)

globalTrackingRegionFromBeamspot = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer", # TODO: import and clone 
    RegionPSet = cms.PSet( 
      nSigmaZ = cms.double( 4.0 ), #TODO: tune 
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      ptMin = cms.double( 0.1 ), # match threshold from ML 
      originRadius = cms.double( 0.02 ), #TODO: tune
      precise = cms.bool( True )
    )
)

trackCollectionKFfromML = cms.EDProducer ("TrackFitterFromML", 
	propagator = cms.string("PropagatorWithMaterial"), 
	oppositePropagator = cms.string("PropagatorWithMaterialOpposite"), 
	ttRecHitBuilder = cms.string("PixelTTRHBuilderWithoutAngle"), 
	#trackerGeometry = cms.InputTag(""),   
	#magneticField = cms.InputTag(""), 
	beamSpot = cms.InputTag("offlineBeamSpot"), 
	trackingRegion = cms.InputTag("GlobalTrackingRegionFromBeamSpotEDProducer")
)


trackFittingKFFromRecHit = cms.Sequence(globalTrackingRegionFromBeamspot+trackCollectionKFfromML)

