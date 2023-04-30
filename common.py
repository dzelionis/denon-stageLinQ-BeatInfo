
# ^\s(\S+)\s=\s'(\S+)',
DECK_COUNT = 2

ANNOUNCEMENT_INTERVAL = 1000 # in ms
LISTEN_PORT = 51337
LISTEN_TIMEOUT = 5000 # in ms
MESSAGE_TIMEOUT = 3000 # in ms
CONNECT_TIMEOUT = 5000 #in ms
DOWNLOAD_TIMEOUT = 10000 # in ms
DISCOVERY_MESSAGE_MARKER = 'airD'
CLIENT_TOKEN = bytearray([82, 253, 252, 7, 33, 130, 101, 79, 22, 63, 95, 15, 154, 98, 29, 114])

quantum = 4.0

## Metronome frequencies
highTone = 1567.98 #Float64
lowTone = 1108.73 #Float64
#  // 100ms click duration
clickDuration = 0.1 # Float64

a = """
const std::size_t kMaxMessageSize = 512;


onst std::vector<uint8_t>& buffer

/*! Utility type to convert between time and sample index given the
 *  time at the beginning of a buffer and the sample rate.
 */
struct SampleTiming
{
  double sampleAtTime(std::chrono::microseconds time) const
  {
    using namespace std::chrono;
    return duration_cast<duration<double>>(time - mBufferBegin).count() * mSampleRate;
  }

  std::chrono::microseconds timeAtSample(const double sample) const
  {
    using namespace std::chrono;
    return mBufferBegin
           + duration_cast<microseconds>(duration<double>{sample / mSampleRate});
  }

  std::chrono::microseconds mBufferBegin;
  double mSampleRate;
};
::":

const UInt32 bufferSize,
examples/LinkHut/LinkHut/AudioEngine.m:    SInt16* buffer)

  // The number of host ticks that elapse between samples
    const Float64 hostTicksPerSample = secondsToHostTime / sampleRate;
examples/LinkHut/LinkHut/AudioEngine.m:        buffer[i] = (SInt16)(32761. * amplitude);

    for (UInt32 i = 0; i < bufferSize; ++i) {
        Float64 amplitude = 0.;
        // Compute the host time for this sample.
        const UInt64 hostTime = beginHostTime + llround(i * hostTicksPerSample);
        const UInt64 lastSampleHostTime = hostTime - llround(hostTicksPerSample);
        // Only make sound for positive beat magnitudes. Negative beat
        // magnitudes are count-in beats.
        if (ABLLinkBeatAtTime(sessionState, hostTime, quantum) >= 0.) {
            // If the phase wraps around between the last sample and the
            // current one with respect to a 1 beat quantum, then a click
            // should occur.
            if (ABLLinkPhaseAtTime(sessionState, hostTime, 1) <
                ABLLinkPhaseAtTime(sessionState, lastSampleHostTime, 1)) {
                *timeAtLastClick = hostTime;
            }

            const Float64 secondsAfterClick =
                (hostTime - *timeAtLastClick) / secondsToHostTime;

            // If we're within the click duration of the last beat, render
            // the click tone into this sample
            if (secondsAfterClick < clickDuration) {
                // If the phase of the last beat with respect to the current
                // quantum was zero, then it was at a quantum boundary and we
                // want to use the high tone. For other beats within the
                // quantum, use the low tone.
                const Float64 freq =
                    floor(ABLLinkPhaseAtTime(sessionState, hostTime, quantum)) == 0
                    ? highTone : lowTone;

                // Simple cosine synth
                amplitude =
                    cos(2 * M_PI * secondsAfterClick * freq) *
                    (1 - sin(5 * M_PI * secondsAfterClick));
            }
        }
        buffer[i] = (SInt16)(32761. * amplitude);
    }
}

_linkData.secondsToHostTime = (1.0e9 * timeInfo.denom) / (Float64)timeInfo.numer;


  inline Float64 ABLLinkBpmInRange(
    const Float64 fromBeat,
    const Float64 toBeat,
    const UInt32 numSamples,
    const Float64 sampleRate) {
    return (toBeat - fromBeat) * sampleRate * 60 / numSamples;
  }




"""


Action =  {
	"Login": "DISCOVERER_HOWDY_",
	"Logout": "DISCOVERER_EXIT_",
}

MessageId = {
	"ServicesAnnouncement" : 0x0,
	"TimeStamp" : 0x1,
	"ServicesRequest" : 0x2,
	"BeatInfoRequest": 0x4,
	"BeatInfoMsg": 0x50,

}

STAGE_LINQ_MAP = {
	"ClientLibrarianDevicesControllerCurrentDevice": "/Client/Librarian/DevicesController/CurrentDevice",
	"ClientLibrarianDevicesControllerHasSDCardConnected": "/Client/Librarian/DevicesController/HasSDCardConnected",
	"ClientLibrarianDevicesControllerHasUsbDeviceConnected": "/Client/Librarian/DevicesController/HasUsbDeviceConnected",
	"ClientPreferencesLayerB": "/Client/Preferences/LayerB",
	"ClientPreferencesPlayer": "/Client/Preferences/Player",
	"ClientPreferencesProfileApplicationPlayerColor1": "/Client/Preferences/Profile/Application/PlayerColor1",
	"ClientPreferencesProfileApplicationPlayerColor1A": "/Client/Preferences/Profile/Application/PlayerColor1A",
	"ClientPreferencesProfileApplicationPlayerColor1B": "/Client/Preferences/Profile/Application/PlayerColor1B",
	"ClientPreferencesProfileApplicationPlayerColor2": "/Client/Preferences/Profile/Application/PlayerColor2",
	"ClientPreferencesProfileApplicationPlayerColor2A": "/Client/Preferences/Profile/Application/PlayerColor2A",
	"ClientPreferencesProfileApplicationPlayerColor2B": "/Client/Preferences/Profile/Application/PlayerColor2B",
	"ClientPreferencesProfileApplicationPlayerColor3": "/Client/Preferences/Profile/Application/PlayerColor3",
	"ClientPreferencesProfileApplicationPlayerColor3A": "/Client/Preferences/Profile/Application/PlayerColor3A",
	"ClientPreferencesProfileApplicationPlayerColor3B": "/Client/Preferences/Profile/Application/PlayerColor3B",
	"ClientPreferencesProfileApplicationPlayerColor4": "/Client/Preferences/Profile/Application/PlayerColor4",
	"ClientPreferencesProfileApplicationPlayerColor4A": "/Client/Preferences/Profile/Application/PlayerColor4A",
	"ClientPreferencesProfileApplicationPlayerColor4B": "/Client/Preferences/Profile/Application/PlayerColor4B",
	"ClientPreferencesProfileApplicationSyncMode": "/Client/Preferences/Profile/Application/SyncMode",
	"EngineDeck1CurrentBPM": "/Engine/Deck1/CurrentBPM",
	"EngineDeck1ExternalMixerVolume": "/Engine/Deck1/ExternalMixerVolume",
	"EngineDeck1ExternalScratchWheelTouch": "/Engine/Deck1/ExternalScratchWheelTouch",
	"EngineDeck1PadsView": "/Engine/Deck1/Pads/View",
	"EngineDeck1Play": "/Engine/Deck1/Play",
	"EngineDeck1PlayState": "/Engine/Deck1/PlayState",
	"EngineDeck1PlayStatePath": "/Engine/Deck1/PlayStatePath",
	"EngineDeck1Speed": "/Engine/Deck1/Speed",
	"EngineDeck1SpeedNeutral": "/Engine/Deck1/SpeedNeutral",
	"EngineDeck1SpeedOffsetDown": "/Engine/Deck1/SpeedOffsetDown",
	"EngineDeck1SpeedOffsetUp": "/Engine/Deck1/SpeedOffsetUp",
	"EngineDeck1SpeedRange": "/Engine/Deck1/SpeedRange",
	"EngineDeck1SpeedState": "/Engine/Deck1/SpeedState",
	"EngineDeck1SyncMode": "/Engine/Deck1/SyncMode",
	"EngineDeck1TrackArtistName": "/Engine/Deck1/Track/ArtistName",
	"EngineDeck1TrackBleep": "/Engine/Deck1/Track/Bleep",
	"EngineDeck1TrackCuePosition": "/Engine/Deck1/Track/CuePosition",
	"EngineDeck1TrackCurrentBPM": "/Engine/Deck1/Track/CurrentBPM",
	"EngineDeck1TrackCurrentKeyIndex": "/Engine/Deck1/Track/CurrentKeyIndex",
	"EngineDeck1TrackCurrentLoopInPosition": "/Engine/Deck1/Track/CurrentLoopInPosition",
	"EngineDeck1TrackCurrentLoopOutPosition": "/Engine/Deck1/Track/CurrentLoopOutPosition",
	"EngineDeck1TrackCurrentLoopSizeInBeats": "/Engine/Deck1/Track/CurrentLoopSizeInBeats",
	"EngineDeck1TrackKeyLock": "/Engine/Deck1/Track/KeyLock",
	"EngineDeck1TrackLoopEnableState": "/Engine/Deck1/Track/LoopEnableState",
	"EngineDeck1TrackLoopQuickLoop1": "/Engine/Deck1/Track/Loop/QuickLoop1",
	"EngineDeck1TrackLoopQuickLoop2": "/Engine/Deck1/Track/Loop/QuickLoop2",
	"EngineDeck1TrackLoopQuickLoop3": "/Engine/Deck1/Track/Loop/QuickLoop3",
	"EngineDeck1TrackLoopQuickLoop4": "/Engine/Deck1/Track/Loop/QuickLoop4",
	"EngineDeck1TrackLoopQuickLoop5": "/Engine/Deck1/Track/Loop/QuickLoop5",
	"EngineDeck1TrackLoopQuickLoop6": "/Engine/Deck1/Track/Loop/QuickLoop6",
	"EngineDeck1TrackLoopQuickLoop7": "/Engine/Deck1/Track/Loop/QuickLoop7",
	"EngineDeck1TrackLoopQuickLoop8": "/Engine/Deck1/Track/Loop/QuickLoop8",
	"EngineDeck1TrackPlayPauseLEDState": "/Engine/Deck1/Track/PlayPauseLEDState",
	"EngineDeck1TrackSampleRate": "/Engine/Deck1/Track/SampleRate",
	"EngineDeck1TrackSongAnalyzed": "/Engine/Deck1/Track/SongAnalyzed",
	"EngineDeck1TrackSongLoaded": "/Engine/Deck1/Track/SongLoaded",
	"EngineDeck1TrackSongName": "/Engine/Deck1/Track/SongName",
	"EngineDeck1TrackSoundSwitchGUID": "/Engine/Deck1/Track/SoundSwitchGuid",
	"EngineDeck1TrackTrackBytes": "/Engine/Deck1/Track/TrackBytes",
	"EngineDeck1TrackTrackData": "/Engine/Deck1/Track/TrackData",
	"EngineDeck1TrackTrackLength": "/Engine/Deck1/Track/TrackLength",
	"EngineDeck1TrackTrackName": "/Engine/Deck1/Track/TrackName",
	"EngineDeck1TrackTrackNetworkPath": "/Engine/Deck1/Track/TrackNetworkPath",
	"EngineDeck1TrackTrackURI": "/Engine/Deck1/Track/TrackUri",
	"EngineDeck1TrackTrackWasPlayed": "/Engine/Deck1/Track/TrackWasPlayed",
	"EngineDeck2CurrentBPM": "/Engine/Deck2/CurrentBPM",
	"EngineDeck2ExternalMixerVolume": "/Engine/Deck2/ExternalMixerVolume",
	"EngineDeck2ExternalScratchWheelTouch": "/Engine/Deck2/ExternalScratchWheelTouch",
	"EngineDeck2PadsView": "/Engine/Deck2/Pads/View",
	"EngineDeck2Play": "/Engine/Deck2/Play",
	"EngineDeck2PlayState": "/Engine/Deck2/PlayState",
	"EngineDeck2PlayStatePath": "/Engine/Deck2/PlayStatePath",
	"EngineDeck2Speed": "/Engine/Deck2/Speed",
	"EngineDeck2SpeedNeutral": "/Engine/Deck2/SpeedNeutral",
	"EngineDeck2SpeedOffsetDown": "/Engine/Deck2/SpeedOffsetDown",
	"EngineDeck2SpeedOffsetUp": "/Engine/Deck2/SpeedOffsetUp",
	"EngineDeck2SpeedRange": "/Engine/Deck2/SpeedRange",
	"EngineDeck2SpeedState": "/Engine/Deck2/SpeedState",
	"EngineDeck2SyncMode": "/Engine/Deck2/SyncMode",
	"EngineDeck2TrackArtistName": "/Engine/Deck2/Track/ArtistName",
	"EngineDeck2TrackBleep": "/Engine/Deck2/Track/Bleep",
	"EngineDeck2TrackCuePosition": "/Engine/Deck2/Track/CuePosition",
	"EngineDeck2TrackCurrentBPM": "/Engine/Deck2/Track/CurrentBPM",
	"EngineDeck2TrackCurrentKeyIndex": "/Engine/Deck2/Track/CurrentKeyIndex",
	"EngineDeck2TrackCurrentLoopInPosition": "/Engine/Deck2/Track/CurrentLoopInPosition",
	"EngineDeck2TrackCurrentLoopOutPosition": "/Engine/Deck2/Track/CurrentLoopOutPosition",
	"EngineDeck2TrackCurrentLoopSizeInBeats": "/Engine/Deck2/Track/CurrentLoopSizeInBeats",
	"EngineDeck2TrackKeyLock": "/Engine/Deck2/Track/KeyLock",
	"EngineDeck2TrackLoopEnableState": "/Engine/Deck2/Track/LoopEnableState",
	"EngineDeck2TrackLoopQuickLoop1": "/Engine/Deck2/Track/Loop/QuickLoop1",
	"EngineDeck2TrackLoopQuickLoop2": "/Engine/Deck2/Track/Loop/QuickLoop2",
	"EngineDeck2TrackLoopQuickLoop3": "/Engine/Deck2/Track/Loop/QuickLoop3",
	"EngineDeck2TrackLoopQuickLoop4": "/Engine/Deck2/Track/Loop/QuickLoop4",
	"EngineDeck2TrackLoopQuickLoop5": "/Engine/Deck2/Track/Loop/QuickLoop5",
	"EngineDeck2TrackLoopQuickLoop6": "/Engine/Deck2/Track/Loop/QuickLoop6",
	"EngineDeck2TrackLoopQuickLoop7": "/Engine/Deck2/Track/Loop/QuickLoop7",
	"EngineDeck2TrackLoopQuickLoop8": "/Engine/Deck2/Track/Loop/QuickLoop8",
	"EngineDeck2TrackPlayPauseLEDState": "/Engine/Deck2/Track/PlayPauseLEDState",
	"EngineDeck2TrackSampleRate": "/Engine/Deck2/Track/SampleRate",
	"EngineDeck2TrackSongAnalyzed": "/Engine/Deck2/Track/SongAnalyzed",
	"EngineDeck2TrackSongLoaded": "/Engine/Deck2/Track/SongLoaded",
	"EngineDeck2TrackSongName": "/Engine/Deck2/Track/SongName",
	"EngineDeck2TrackSoundSwitchGUID": "/Engine/Deck2/Track/SoundSwitchGuid",
	"EngineDeck2TrackTrackBytes": "/Engine/Deck2/Track/TrackBytes",
	"EngineDeck2TrackTrackData": "/Engine/Deck2/Track/TrackData",
	"EngineDeck2TrackTrackLength": "/Engine/Deck2/Track/TrackLength",
	"EngineDeck2TrackTrackName": "/Engine/Deck2/Track/TrackName",
	"EngineDeck2TrackTrackNetworkPath": "/Engine/Deck2/Track/TrackNetworkPath",
	"EngineDeck2TrackTrackURI": "/Engine/Deck2/Track/TrackUri",
	"EngineDeck2TrackTrackWasPlayed": "/Engine/Deck2/Track/TrackWasPlayed",
	"EngineDeck3CurrentBPM": "/Engine/Deck3/CurrentBPM",
	"EngineDeck3ExternalMixerVolume": "/Engine/Deck3/ExternalMixerVolume",
	"EngineDeck3ExternalScratchWheelTouch": "/Engine/Deck3/ExternalScratchWheelTouch",
	"EngineDeck3PadsView": "/Engine/Deck3/Pads/View",
	"EngineDeck3Play": "/Engine/Deck3/Play",
	"EngineDeck3PlayState": "/Engine/Deck3/PlayState",
	"EngineDeck3PlayStatePath": "/Engine/Deck3/PlayStatePath",
	"EngineDeck3Speed": "/Engine/Deck3/Speed",
	"EngineDeck3SpeedNeutral": "/Engine/Deck3/SpeedNeutral",
	"EngineDeck3SpeedOffsetDown": "/Engine/Deck3/SpeedOffsetDown",
	"EngineDeck3SpeedOffsetUp": "/Engine/Deck3/SpeedOffsetUp",
	"EngineDeck3SpeedRange": "/Engine/Deck3/SpeedRange",
	"EngineDeck3SpeedState": "/Engine/Deck3/SpeedState",
	"EngineDeck3SyncMode": "/Engine/Deck3/SyncMode",
	"EngineDeck3TrackArtistName": "/Engine/Deck3/Track/ArtistName",
	"EngineDeck3TrackBleep": "/Engine/Deck3/Track/Bleep",
	"EngineDeck3TrackCuePosition": "/Engine/Deck3/Track/CuePosition",
	"EngineDeck3TrackCurrentBPM": "/Engine/Deck3/Track/CurrentBPM",
	"EngineDeck3TrackCurrentKeyIndex": "/Engine/Deck3/Track/CurrentKeyIndex",
	"EngineDeck3TrackCurrentLoopInPosition": "/Engine/Deck3/Track/CurrentLoopInPosition",
	"EngineDeck3TrackCurrentLoopOutPosition": "/Engine/Deck3/Track/CurrentLoopOutPosition",
	"EngineDeck3TrackCurrentLoopSizeInBeats": "/Engine/Deck3/Track/CurrentLoopSizeInBeats",
	"EngineDeck3TrackKeyLock": "/Engine/Deck3/Track/KeyLock",
	"EngineDeck3TrackLoopEnableState": "/Engine/Deck3/Track/LoopEnableState",
	"EngineDeck3TrackLoopQuickLoop1": "/Engine/Deck3/Track/Loop/QuickLoop1",
	"EngineDeck3TrackLoopQuickLoop2": "/Engine/Deck3/Track/Loop/QuickLoop2",
	"EngineDeck3TrackLoopQuickLoop3": "/Engine/Deck3/Track/Loop/QuickLoop3",
	"EngineDeck3TrackLoopQuickLoop4": "/Engine/Deck3/Track/Loop/QuickLoop4",
	"EngineDeck3TrackLoopQuickLoop5": "/Engine/Deck3/Track/Loop/QuickLoop5",
	"EngineDeck3TrackLoopQuickLoop6": "/Engine/Deck3/Track/Loop/QuickLoop6",
	"EngineDeck3TrackLoopQuickLoop7": "/Engine/Deck3/Track/Loop/QuickLoop7",
	"EngineDeck3TrackLoopQuickLoop8": "/Engine/Deck3/Track/Loop/QuickLoop8",
	"EngineDeck3TrackPlayPauseLEDState": "/Engine/Deck3/Track/PlayPauseLEDState",
	"EngineDeck3TrackSampleRate": "/Engine/Deck3/Track/SampleRate",
	"EngineDeck3TrackSongAnalyzed": "/Engine/Deck3/Track/SongAnalyzed",
	"EngineDeck3TrackSongLoaded": "/Engine/Deck3/Track/SongLoaded",
	"EngineDeck3TrackSongName": "/Engine/Deck3/Track/SongName",
	"EngineDeck3TrackSoundSwitchGUID": "/Engine/Deck3/Track/SoundSwitchGuid",
	"EngineDeck3TrackTrackBytes": "/Engine/Deck3/Track/TrackBytes",
	"EngineDeck3TrackTrackData": "/Engine/Deck3/Track/TrackData",
	"EngineDeck3TrackTrackLength": "/Engine/Deck3/Track/TrackLength",
	"EngineDeck3TrackTrackName": "/Engine/Deck3/Track/TrackName",
	"EngineDeck3TrackTrackNetworkPath": "/Engine/Deck3/Track/TrackNetworkPath",
	"EngineDeck3TrackTrackURI": "/Engine/Deck3/Track/TrackUri",
	"EngineDeck3TrackTrackWasPlayed": "/Engine/Deck3/Track/TrackWasPlayed",
	"EngineDeck4CurrentBPM": "/Engine/Deck4/CurrentBPM",
	"EngineDeck4ExternalMixerVolume": "/Engine/Deck4/ExternalMixerVolume",
	"EngineDeck4ExternalScratchWheelTouch": "/Engine/Deck4/ExternalScratchWheelTouch",
	"EngineDeck4PadsView": "/Engine/Deck4/Pads/View",
	"EngineDeck4Play": "/Engine/Deck4/Play",
	"EngineDeck4PlayState": "/Engine/Deck4/PlayState",
	"EngineDeck4PlayStatePath": "/Engine/Deck4/PlayStatePath",
	"EngineDeck4Speed": "/Engine/Deck4/Speed",
	"EngineDeck4SpeedNeutral": "/Engine/Deck4/SpeedNeutral",
	"EngineDeck4SpeedOffsetDown": "/Engine/Deck4/SpeedOffsetDown",
	"EngineDeck4SpeedOffsetUp": "/Engine/Deck4/SpeedOffsetUp",
	"EngineDeck4SpeedRange": "/Engine/Deck4/SpeedRange",
	"EngineDeck4SpeedState": "/Engine/Deck4/SpeedState",
	"EngineDeck4SyncMode": "/Engine/Deck4/SyncMode",
	"EngineDeck4TrackArtistName": "/Engine/Deck4/Track/ArtistName",
	"EngineDeck4TrackBleep": "/Engine/Deck4/Track/Bleep",
	"EngineDeck4TrackCuePosition": "/Engine/Deck4/Track/CuePosition",
	"EngineDeck4TrackCurrentBPM": "/Engine/Deck4/Track/CurrentBPM",
	"EngineDeck4TrackCurrentKeyIndex": "/Engine/Deck4/Track/CurrentKeyIndex",
	"EngineDeck4TrackCurrentLoopInPosition": "/Engine/Deck4/Track/CurrentLoopInPosition",
	"EngineDeck4TrackCurrentLoopOutPosition": "/Engine/Deck4/Track/CurrentLoopOutPosition",
	"EngineDeck4TrackCurrentLoopSizeInBeats": "/Engine/Deck4/Track/CurrentLoopSizeInBeats",
	"EngineDeck4TrackKeyLock": "/Engine/Deck4/Track/KeyLock",
	"EngineDeck4TrackLoopEnableState": "/Engine/Deck4/Track/LoopEnableState",
	"EngineDeck4TrackLoopQuickLoop1": "/Engine/Deck4/Track/Loop/QuickLoop1",
	"EngineDeck4TrackLoopQuickLoop2": "/Engine/Deck4/Track/Loop/QuickLoop2",
	"EngineDeck4TrackLoopQuickLoop3": "/Engine/Deck4/Track/Loop/QuickLoop3",
	"EngineDeck4TrackLoopQuickLoop4": "/Engine/Deck4/Track/Loop/QuickLoop4",
	"EngineDeck4TrackLoopQuickLoop5": "/Engine/Deck4/Track/Loop/QuickLoop5",
	"EngineDeck4TrackLoopQuickLoop6": "/Engine/Deck4/Track/Loop/QuickLoop6",
	"EngineDeck4TrackLoopQuickLoop7": "/Engine/Deck4/Track/Loop/QuickLoop7",
	"EngineDeck4TrackLoopQuickLoop8": "/Engine/Deck4/Track/Loop/QuickLoop8",
	"EngineDeck4TrackPlayPauseLEDState": "/Engine/Deck4/Track/PlayPauseLEDState",
	"EngineDeck4TrackSampleRate": "/Engine/Deck4/Track/SampleRate",
	"EngineDeck4TrackSongAnalyzed": "/Engine/Deck4/Track/SongAnalyzed",
	"EngineDeck4TrackSongLoaded": "/Engine/Deck4/Track/SongLoaded",
	"EngineDeck4TrackSongName": "/Engine/Deck4/Track/SongName",
	"EngineDeck4TrackSoundSwitchGUID": "/Engine/Deck4/Track/SoundSwitchGuid",
	"EngineDeck4TrackTrackBytes": "/Engine/Deck4/Track/TrackBytes",
	"EngineDeck4TrackTrackData": "/Engine/Deck4/Track/TrackData",
	"EngineDeck4TrackTrackLength": "/Engine/Deck4/Track/TrackLength",
	"EngineDeck4TrackTrackName": "/Engine/Deck4/Track/TrackName",
	"EngineDeck4TrackTrackNetworkPath": "/Engine/Deck4/Track/TrackNetworkPath",
	"EngineDeck4TrackTrackURI": "/Engine/Deck4/Track/TrackUri",
	"EngineDeck4TrackTrackWasPlayed": "/Engine/Deck4/Track/TrackWasPlayed",
	"EngineDeckCount": "/Engine/DeckCount",
	"GUIDecksDeckActiveDeck": "/GUI/Decks/Deck/ActiveDeck",
	"GUIViewLayerLayerB": "/GUI/ViewLayer/LayerB",
	"MixerCH1faderPosition": "/Mixer/CH1faderPosition",
	"MixerCH2faderPosition": "/Mixer/CH2faderPosition",
	"MixerCH3faderPosition": "/Mixer/CH3faderPosition",
	"MixerCH4faderPosition": "/Mixer/CH4faderPosition",
	"MixerCrossfaderPosition": "/Mixer/CrossfaderPosition",
}
