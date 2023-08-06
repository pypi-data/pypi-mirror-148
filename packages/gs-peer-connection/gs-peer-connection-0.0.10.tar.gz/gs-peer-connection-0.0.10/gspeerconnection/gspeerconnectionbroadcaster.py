import ast
import json
import logging
import platform

import socketio
from aiortc import RTCPeerConnection, RTCRtpSender, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaPlayer, MediaRelay

raspberry = True

relay = None
webcam = None
camera = None
videotrack = None


class GSPeerConnectionBroadcaster:

    def create_local_tracks_new(self, play_from, decode):
        global relay, webcam

        if play_from:
            player = MediaPlayer(play_from, decode=decode)
            return player.audio, player.video
        else:
            options = {"framerate": str(self.gsdbs.credentials["framerate"]),
                       "video_size": f"{str(self.gsdbs.credentials['hres'])}x{str(self.gsdbs.credentials['vres'])}",
                       "b:v": f" {self.gsdbs.credentials['hres'] * self.gsdbs.credentials['vres'] * self.gsdbs.credentials['framerate'] * 0.150}"}
            if relay is None:
                if platform.system() == "Darwin":
                    webcam = MediaPlayer(
                        "default:none", format="avfoundation", options=options
                    )
                elif platform.system() == "Windows":
                    webcam = MediaPlayer(
                        f"video={self.gsdbs.credentials['device']}", format="dshow", options=options
                    )
                else:
                    webcam = MediaPlayer(f"{self.gsdbs.credentials['device']}", format="v4l2", options=options)
                relay = MediaRelay()
            return None, relay.subscribe(webcam.video)

    def force_codec(self, pc, sender, forced_codec):
        kind = forced_codec.split("/")[0]
        codecs = RTCRtpSender.getCapabilities(kind).codecs
        transceiver = next(t for t in pc.getTransceivers() if t.sender == sender)
        transceiver.setCodecPreferences(
            [codec for codec in codecs if codec.mimeType == forced_codec]
        )

    @classmethod
    async def create(cls, gsdbs):
        self = GSPeerConnectionBroadcaster()
        self.gsdbs = gsdbs
        self.sio = socketio.AsyncClient()
        self.peerConnections = {}
        self._logger = logging.getLogger(__name__)
        self.webcam = None
        self.relay = None

        @self.sio.event
        async def connect():
            self._logger.info('connection established')

        @self.sio.event
        async def answer(id, description):
            if type(description) == str:
                description = ast.literal_eval(description)
            desc = type('new_dict', (object,), description)
            await self.peerConnections[id].setRemoteDescription(desc)

        @self.sio.event
        async def watcher(id):
            pc = RTCPeerConnection(configuration=RTCConfiguration([
                RTCIceServer("stun:stun.l.google:19302"),
                RTCIceServer(self.gsdbs.credentials["turnserver"],
                             self.gsdbs.credentials["turnuser"],
                             self.gsdbs.credentials["turnpw"]),
            ]))
            self.peerConnections[id] = pc

            audio, video = self.create_local_tracks_new(
                None, decode=self.gsdbs.credentials["decode"]
            )
            video_codec = self.gsdbs.credentials["videocodec"]

            if audio:
                pc.addTrack(audio)
            if video:
                video_sender = pc.addTrack(video)
                if video_codec:
                    self.force_codec(pc, video_sender, video_codec)
                    # only allow the specified video codec


            @pc.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                # self._logger.info("ICE connection state is %s", pc.iceConnectionState)
                if pc.iceConnectionState == "failed":
                    await pc.close()
                    self.peerConnections.pop(id, None)

            await pc.setLocalDescription(await pc.createOffer())
            await self.sio.emit("offer", {"id": id,
                                          "message": json.dumps(
                                              {"type": pc.localDescription.type, "sdp": pc.localDescription.sdp})})
            # self._logger.info(pc.signalingState)

        @self.sio.event
        async def disconnectPeer(id):
            if id in self.peerConnections:
                await self.peerConnections[id].close()
                self.peerConnections.pop(id, None)

        @self.sio.event
        async def disconnect():
            self._logger.info('disconnected from server')

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}')
        await self.sio.wait()
