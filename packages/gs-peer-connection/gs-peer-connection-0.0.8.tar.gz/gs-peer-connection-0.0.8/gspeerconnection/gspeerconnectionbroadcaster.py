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

    def create_local_tracks(self, device, transcode=True):
        global relay, webcam
        if relay is None:
            if platform.system() == "Darwin":
                options = {
                    "video_size": f"{str(self.gsdbs.credentials['hres'])}x{str(self.gsdbs.credentials['vres'])}",
                    "preset": "veryfast",
                    "framerate": str(self.gsdbs.credentials["framerate"]),
                    "c:v": "h264_v4l2m2m",
                    "input_format": "h264",
                    "pixelformat": "H264"
                }
                webcam = MediaPlayer("default:none", format="avfoundation", options=options)
            elif platform.system() == "Windows":
                webcam = MediaPlayer(f"video={device}", format="dshow")
            else:
                options = {
                    "video_size": f"{str(self.gsdbs.credentials['hres'])}x{str(self.gsdbs.credentials['vres'])}",
                    "preset": "veryfast",
                    "framerate": str(self.gsdbs.credentials["framerate"]),
                    "c:v": "h264_v4l2m2m",
                    "input_format": "h264",
                    "pixelformat": "H264"
                }
                webcam = MediaPlayer(device, format="v4l2", options=options)
            relay = MediaRelay()
        return relay.subscribe(webcam.video, buffered=False)

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
                None, decode=True
            )
            channel = pc.createDataChannel("message")

            # def send_data():
            #     channel.send("test123")
            # channel.on("open", send_data)

            video_codec = "video/H264"

            if audio:
                pc.addTrack(audio)
            if video:
                video_sender = pc.addTrack(video)
                if video_codec:
                    # only allow the specified video codec
                    video_codecs = RTCRtpSender.getCapabilities("video").codecs
                    video_transceiver = next(
                        t for t in pc.getTransceivers() if t.sender == video_sender
                    )
                    video_transceiver.setCodecPreferences(
                        [codec for codec in video_codecs if codec.mimeType == video_codec]
                    )

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
