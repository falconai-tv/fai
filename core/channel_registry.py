from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Channel:
    name: str
    url: str
    category: str = "general"
    language: str = "multi"
    country: str = "global"
    tags: Optional[List[str]] = None
    is_live: bool = True

CHANNELS = [
    Channel(
        "DW News",
        "https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/master.m3u8",
        category="news",
        language="en",
        country="germany",
        tags=["world", "politics", "europe", "germany"]
    ),
    Channel(
        "TRT World",
        "https://tv-trtworld.medya.trt.com.tr/master.m3u8",
        category="news",
        language="en",
        country="turkey",
        tags=["world", "middle east", "politics"]
    ),
    Channel(
        "Africa News",
        "https://euronews-africanews-1-us.samsung.wurl.com/manifest/playlist.m3u8",
        category="news",
        language="en",
        country="france",
        tags=["africa", "world", "news"]
    ),
    Channel(
        "NASA TV",
        "https://ntvpublic-v2.akamaized.net/hls/live/2028660/NTV-Public-V2/master.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["space", "science", "education"]
    ),
    Channel(
        "CBN",
        "https://fastly.live.brightcove.com/6380396819112/us-east-1/734546207001/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJob3N0IjoiczFpM3ZpLmVncmVzcy50N2M3emwiLCJhY2NvdW50X2lkIjoiNzM0NTQ2MjA3MDAxIiwiZWhuIjoiZmFzdGx5LmxpdmUuYnJpZ2h0Y292ZS5jb20iLCJpc3MiOiJibGl2ZS1wbGF5YmFjay1zb3VyY2UtYXBpIiwic3ViIjoicGF0aG1hcHRva2VuIiwiYXVkIjpbIjczNDU0NjIwNzAwMSJdLCJqdGkiOiI2MzgwMzk2ODE5MTEyIn0.GDYp4IWtzwPkupEWeeOavnioVknO-Ev3UGlHvM1rE6I/playlist-hls.m3u8",
        category="religion",
        language="en",
        country="usa",
        tags=["christian", "faith", "news"]
    ),
    Channel(
        "1-2-3 TV",
        "https://123tv-mx1.flex-cdn.net/index.m3u8",
        category="entertainment",
        language="es",
        country="mexico",
        tags=["variety", "tv"]
    ),
    Channel(
        "Allgäu TV",
        "https://stream01.welocal.stream/stream/fhd-allgaeutv_25679/ngrp:stream_all/playlist.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["local", "germany", "news"]
    ),
    Channel(
        "Altenburg TV",
        "https://58de7a369a9c4.streamlock.net/abgtv/abgtv_1080p/playlist.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["local", "news"]
    ),
    Channel(
        "ANIMAL KINGDOM",
        "https://cdn6.goprimetime.info/feed/202306140918/LC18/index.m3u8",
        category="kids",
        language="en",
        country="global",
        tags=["animals", "nature"]
    ),

    Channel(
        "Anixe +",
        "https://ma.anixa.tv/clips/stream/anixesd/index.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["movies", "tv"]
    ),

    Channel(
        "Anixe HD Serie",
        "https://ma.anixa.tv/clips/stream/anixehd/index.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["series"]
    ),

    Channel(
        "Bibel TV",
        "https://bibint01.iptv-playoutcenter.de/bibint01/bibint01.stream_all/playlist.m3u8",
        category="religion",
        language="de",
        country="germany",
        tags=["christian"]
    ),

    Channel(
        "BR Fernsehen Nord",
        "https://mcdn.br.de/br/fs/bfs_nord/hls/de/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),
    Channel(
        "Das Erste HD",
        "https://daserste-live.ard-mcdn.de/daserste/live/hls/int/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["germany", "public tv", "news"]
    ),

    Channel(
        "Deluxe Dance",
        "https://sdn-global-live-streaming-packager-cache.3qsdn.com/64733/64733_264_live.m3u8",
        category="music",
        language="en",
        country="germany",
        tags=["dance", "music"]
    ),

    Channel(
        "Deluxe Music",
        "https://sdn-global-live-streaming-packager-cache.3qsdn.com/13456/13456_264_live.m3u8",
        category="music",
        language="en",
        country="germany",
        tags=["music", "pop"]
    ),

    Channel(
        "DW English",
        "https://dwamdstream102.akamaized.net/hls/live/2015525/dwstream102/master.m3u8",
        category="news",
        language="en",
        country="germany",
        tags=["world", "news"]
    ),

    Channel(
        "DW Arabic",
        "https://dwamdstream103.akamaized.net/hls/live/2015526/dwstream103/master.m3u8",
        category="news",
        language="ar",
        country="germany",
        tags=["world", "middle east", "news"]
    ),

    Channel(
        "HSE 24",
        "https://hse24.akamaized.net/hls/live/2006663/hse24/playlist.m3u8",
        category="shopping",
        language="de",
        country="germany",
        tags=["shopping"]
    ),

    Channel(
        "Deluxe Rap",
        "https://sdn-global-live-streaming-packager-cache.3qsdn.com/65183/65183_264_live.m3u8",
        category="music",
        language="en",
        country="germany",
        tags=["rap", "hiphop", "music"]
    ),

    Channel(
        "Hope Channel German",
        "https://customer-x8zydurm357k8j9p.cloudflarestream.com/5b46490d20cdd87fcac238b0027813e0/manifest/video.m3u8",
        category="religion",
        language="de",
        country="germany",
        tags=["christian"]
    ),

    Channel(
        "Hamburg 1",
        "https://stream.hamburg1.de/live_abr/hamburg1_abr/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "news"]
    ),

    Channel(
        "KaufBei TV",
        "https://api.alpaca.t62a.com/hls/9103/index.m3u8",
        category="shopping",
        language="de",
        country="germany",
        tags=["shopping", "tv"]
    ),
    Channel(
        "KiKA (Official)",
        "https://kikahls.akamaized.net/hls/live/2022690/livetvkika_ww/master.m3u8",
        category="kids",
        language="de",
        country="germany",
        tags=["kids", "cartoons"]
    ),

    Channel(
        "L-TV",
        "https://live2.telvi.de/hls/l-tv_s1.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "Leipzig Fernsehen",
        "https://leipzig.iptv-playoutcenter.de/leipzig/leipzigfernsehen.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "news"]
    ),

    Channel(
        "Magenta Musik 360",
        "https://streaming.magentamusik.de/csm/573870/magentamusik1/index.m3u8",
        category="music",
        language="en",
        country="germany",
        tags=["music", "live"]
    ),

    Channel(
        "NDR Hamburg",
        "https://mcdn.ndr.de/ndr/hls/ndr_fs/ndr_hh/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "NDR Mecklenburg-Vorpommern",
        "https://mcdn.ndr.de/ndr/hls/ndr_fs/ndr_mv/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "NDR Niedersachsen",
        "https://mcdn.ndr.de/ndr/hls/ndr_fs/ndr_nds/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "NDR Schleswig-Holstein",
        "https://mcdn.ndr.de/ndr/hls/ndr_fs/ndr_sh/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "Nick Germany (Airspace)",
        "https://0d26a00dfbb1.airspace-cdn.cbsivideo.com/nick1999/master/nick1999.m3u8",
        category="kids",
        language="de",
        country="germany",
        tags=["kids", "cartoons"]
    ),

    Channel(
        "Niederbayern TV",
        "https://stream03.welocal.stream/stream/sat-nby/ngrp:sat-nby.stream_all/index.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "NRWision",
        "https://fms.nrwision.de/live/ngrp:livestreamHD.stream/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "education"]
    ),
    Channel(
        "Al Jazeera",
        "https://live-hls-web-aje.getaj.net/AJE/index.m3u8",
        category="news",
        language="en",
        country="qatar",
        tags=["middle east", "war", "global"]
    ),

    Channel(
        "France 24",
        "https://live.france24.com/hls/live/2037179/F24_FR_HI_HLS/master_5000.m3u8",
        category="news",
        language="fr",
        country="france",
        tags=["europe", "world"]
    ),

    Channel(
        "ZDF",
        "https://zdf-hls-15.akamaized.net/hls/live/2016498/de/high/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["germany", "news"]
    ),

    Channel(
        "ONE1 Music",
        "https://cdne.folxplay.tv/folx-trz/streams/ch-3/master.m3u8",
        category="music",
        language="en",
        country="global",
        tags=["music"]
    ),

    Channel(
        "One Adria",
        "https://cdne.folxplay.tv/folx-trz/streams/ch-6/master.m3u8",
        category="music",
        language="sq",
        country="balkan",
        tags=["music", "balkan"]
    ),

    Channel(
        "QVC Germany",
        "https://qvcde-live.akamaized.net/hls/live/2097104/qvc/master.m3u8",
        category="shopping",
        language="de",
        country="germany",
        tags=["shopping"]
    ),

    Channel(
        "Radio 21 TV",
        "https://live.creacast.com/radio21/smil:radio21.smil/playlist.m3u8",
        category="music",
        language="de",
        country="germany",
        tags=["radio", "music"]
    ),

    Channel(
        "OK Kiel",
        "https://live-cdn.oksh.de/play/hls/kieltv/index.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "community"]
    ),

    Channel(
        "OK Magdeburg",
        "https://58bd5b7a98e04.streamlock.net/medienasa-live/mp4:ok-magdeburg_high/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "community"]
    ),

    Channel(
        "Parlamentsfernsehen 1",
        "https://cldf-hlsgw.r53.cdn.tv1.eu/1000153copo/hk1.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["politics", "parliament"]
    ),

    Channel(
        "Phoenix (ZDF Official)",
        "https://zdf-hls-19.akamaized.net/hls/live/2016502/de/high/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["politics", "documentary"]
    ),

    Channel(
        "RBB Berlin",
        "https://rbb-hls-berlin.akamaized.net/hls/live/2017824/rbb_berlin/index.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "RBB Brandenburg",
        "https://rbb-hls-brandenburg.akamaized.net/hls/live/2017825/rbb_brandenburg/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "Regio TV Bodensee",
        "https://regiotv-b.iptv-playoutcenter.de/regiotv-b/regiotv-b.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "Regio TV Stuttgart",
        "https://regiotv-s.iptv-playoutcenter.de/regiotv-s/regiotv-s.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "RiC TV",
        "https://rictv.iptv-playoutcenter.de/rictv/rictv-web/playlist.m3u8",
        category="kids",
        language="de",
        country="germany",
        tags=["kids", "family"]
    ),

    Channel(
        "RNF (Rhein-Neckar)",
        "https://rnf.iptv-playoutcenter.de/rnf/rnf.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "Saarland Fernsehen 1",
        "https://saarland1.iptv-playoutcenter.de/saarland1/saarland1.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "Sachsen Eins",
        "https://sachsen1.iptv-playoutcenter.de/sachsen1/sachsen1.stream_1/playlist.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "Sachsen Fernsehen Vogtland",
        "https://vogtland.iptv-playoutcenter.de/vogtland/vogtlandfernsehen.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "news"]
    ),

    Channel(
        "One Adria",
        "https://cdne.folxplay.tv/folx-trz/streams/ch-6/master.m3u8",
        category="music",
        language="multi",
        country="balkan",
        tags=["music", "balkan"]
    ),

    Channel(
        "QVC Germany",
        "https://qvcde-live.akamaized.net/hls/live/2097104/qvc/master.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["shopping", "tv"]
    ),

    Channel(
        "Radio 21 TV",
        "https://live.creacast.com/radio21/smil:radio21.smil/playlist.m3u8",
        category="music",
        language="de",
        country="germany",
        tags=["radio", "music"]
    ),

    Channel(
        "OK Kiel",
        "https://live-cdn.oksh.de/play/hls/kieltv/index.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "community"]
    ),

    Channel(
        "OK Magdeburg",
        "https://58bd5b7a98e04.streamlock.net/medienasa-live/mp4:ok-magdeburg_high/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "community"]
    ),

    Channel(
        "Parlamentsfernsehen 1",
        "https://cldf-hlsgw.r53.cdn.tv1.eu/1000153copo/hk1.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["politics", "parliament"]
    ),

    Channel(
        "Phoenix (ZDF Official)",
        "https://zdf-hls-19.akamaized.net/hls/live/2016502/de/high/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["politics", "documentary"]
    ),

    Channel(
        "RBB Berlin",
        "https://rbb-hls-berlin.akamaized.net/hls/live/2017824/rbb_berlin/index.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["berlin", "regional"]
    ),

    Channel(
        "RBB Brandenburg",
        "https://rbb-hls-brandenburg.akamaized.net/hls/live/2017825/rbb_brandenburg/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["brandenburg", "regional"]
    ),

    Channel(
        "Regio TV Bodensee",
        "https://regiotv-b.iptv-playoutcenter.de/regiotv-b/regiotv-b.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "bodensee"]
    ),

    Channel(
        "Regio TV Stuttgart",
        "https://regiotv-s.iptv-playoutcenter.de/regiotv-s/regiotv-s.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "stuttgart"]
    ),

    Channel(
        "RiC TV",
        "https://rictv.iptv-playoutcenter.de/rictv/rictv-web/playlist.m3u8",
        category="kids",
        language="de",
        country="germany",
        tags=["kids", "family"]
    ),

    Channel(
        "RNF (Rhein-Neckar)",
        "https://rnf.iptv-playoutcenter.de/rnf/rnf.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "rhein-neckar"]
    ),

    Channel(
        "Saarland Fernsehen 1",
        "https://saarland1.iptv-playoutcenter.de/saarland1/saarland1.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "saarland"]
    ),

    Channel(
        "Sachsen Eins",
        "https://sachsen1.iptv-playoutcenter.de/sachsen1/sachsen1.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "sachsen"]
    ),

    Channel(
        "Sachsen Fernsehen Vogtland",
        "https://vogtland.iptv-playoutcenter.de/vogtland/vogtlandfernsehen.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "vogtland"]
    ),

    Channel(
        "Schlager Deluxe",
        "https://sdn-global-live-streaming-packager-cache.3qsdn.com/26658/26658_264_live.m3u8",
        category="music",
        language="de",
        country="germany",
        tags=["music", "schlager"]
    ),

    Channel(
        "Sonnenklar TV",
        "http://euvia.cdn.ses-ps.com/HLS-Live/index.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["travel", "shopping"]
    ),

    Channel(
        "Tagesschau 24",
        "https://tagesschau.akamaized.net/hls/live/2020115/tagesschau/tagesschau_1/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["news", "breaking"]
    ),

    Channel(
        "WDR Fernsehen (Official)",
        "https://wdr-live.ard-mcdn.de/wdr/live/hls/de/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional", "nrw"]
    ),

    Channel(
        "Das Erste",
        "https://daserste-live.ard-mcdn.de/daserste/live/hls/int/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["germany", "public tv"]
    ),

    Channel(
        "QVC Germany",
        "https://qvcde-live.akamaized.net/hls/live/2097104/qvc/master.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["shopping", "tv"]
    ),

    Channel(
        "Radio 21 TV",
        "https://live.creacast.com/radio21/smil:radio21.smil/playlist.m3u8",
        category="music",
        language="de",
        country="germany",
        tags=["radio", "music"]
    ),

    Channel(
        "OK Kiel",
        "https://live-cdn.oksh.de/play/hls/kieltv/index.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "community"]
    ),

    Channel(
        "OK Magdeburg",
        "https://58bd5b7a98e04.streamlock.net/medienasa-live/mp4:ok-magdeburg_high/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["local", "community"]
    ),

    Channel(
        "Parlamentsfernsehen 1",
        "https://cldf-hlsgw.r53.cdn.tv1.eu/1000153copo/hk1.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["politics", "parliament"]
    ),

    Channel(
        "Phoenix (ZDF Official)",
        "https://zdf-hls-19.akamaized.net/hls/live/2016502/de/high/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["politics", "documentary"]
    ),

    Channel(
        "RBB Berlin",
        "https://rbb-hls-berlin.akamaized.net/hls/live/2017824/rbb_berlin/index.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["berlin", "regional"]
    ),

    Channel(
        "RBB Brandenburg",
        "https://rbb-hls-brandenburg.akamaized.net/hls/live/2017825/rbb_brandenburg/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["brandenburg", "regional"]
    ),

    Channel(
        "Regio TV Bodensee",
        "https://regiotv-b.iptv-playoutcenter.de/regiotv-b/regiotv-b.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "Regio TV Stuttgart",
        "https://regiotv-s.iptv-playoutcenter.de/regiotv-s/regiotv-s.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "RiC TV",
        "https://rictv.iptv-playoutcenter.de/rictv/rictv-web/playlist.m3u8",
        category="kids",
        language="de",
        country="germany",
        tags=["kids", "family"]
    ),

    Channel(
        "RNF (Rhein-Neckar)",
        "https://rnf.iptv-playoutcenter.de/rnf/rnf.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "Saarland Fernsehen 1",
        "https://saarland1.iptv-playoutcenter.de/saarland1/saarland1.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "Sachsen Eins",
        "https://sachsen1.iptv-playoutcenter.de/sachsen1/sachsen1.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "Sachsen Fernsehen Vogtland",
        "https://vogtland.iptv-playoutcenter.de/vogtland/vogtlandfernsehen.stream_1/playlist.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "Schlager Deluxe",
        "https://sdn-global-live-streaming-packager-cache.3qsdn.com/26658/26658_264_live.m3u8",
        category="music",
        language="de",
        country="germany",
        tags=["music"]
    ),

    Channel(
        "Sonnenklar TV",
        "http://euvia.cdn.ses-ps.com/HLS-Live/index.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["travel", "shopping"]
    ),

    Channel(
        "Tagesschau 24",
        "https://tagesschau.akamaized.net/hls/live/2020115/tagesschau/tagesschau_1/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["news"]
    ),

    Channel(
        "WDR Fernsehen (Official)",
        "https://wdr-live.ard-mcdn.de/wdr/live/hls/de/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["regional"]
    ),

    Channel(
        "ZDF (Official)",
        "https://zdf-hls-15.akamaized.net/hls/live/2016498/de/high/master.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["public tv"]
    ),

    Channel(
        "ZDFinfo (Official)",
        "https://zdf-hls-17.akamaized.net/hls/live/2016500/de/high/master.m3u8",
        category="documentary",
        language="de",
        country="germany",
        tags=["history", "science"]
    ),

    Channel(
        "Welt der Wunder TV",
        "https://wdw.iptv-playoutcenter.de/wdw/wdw1/playlist.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["science", "knowledge"]
    ),

    Channel(
        "SWR 3 Visual Radio",
        "https://swrswr3vr-hls.akamaized.net/hls/live/2018683/swr3vr/master.m3u8",
        category="music",
        language="de",
        country="germany",
        tags=["radio", "music"]
    ),

    Channel(
        "TV Berlin",
        "https://live2.telvi.de/hls/tvberlin.m3u8",
        category="news",
        language="de",
        country="germany",
        tags=["berlin", "local"]
    ),

    Channel(
        "ZDFneo (Official)",
        "https://zdf-hls-16.akamaized.net/hls/live/2016499/de/high/master.m3u8",
        category="entertainment",
        language="de",
        country="germany",
        tags=["series", "tv"]
    ),

    Channel(
        "ZWEI2 Music",
        "https://cdne.folxplay.tv/folx-trz/streams/ch-2/master.m3u8",
        category="music",
        language="multi",
        country="global",
        tags=["music"]
    ),

    Channel(
        "ABC News Live",
        "https://content.uplynk.com/channel/3324f2467c414329b3b0cc5cd987b6be.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["breaking", "world"]
    ),

    Channel(
        "Alhurra TV",
        "https://mbn-ingest-worldsafe.akamaized.net/hls/live/2038900/MBN_Alhurra_Worldsafe_HLS/master.m3u8",
        category="news",
        language="ar",
        country="usa",
        tags=["middle east"]
    ),

    Channel(
        "Alhurra Iraq",
        "https://mbn-ingest-worldsafe.akamaized.net/hls/live/2038899/MBN_Iraq_Worldsafe_HLS/master.m3u8",
        category="news",
        language="ar",
        country="iraq",
        tags=["iraq", "news"]
    ),
    Channel(
        "Comet",
        "https://fast-channels.sinclairstoryline.com/COMET/index.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["movies", "sci-fi"]
    ),

    Channel(
        "Classic Arts Showcase",
        "https://classicarts.akamaized.net/hls/live/1024257/CAS/master.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["arts", "culture"]
    ),

    Channel(
        "Dateline 24/7",
        "https://dz59iptwz5rxs.cloudfront.net/live/master.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["crime", "documentary"]
    ),

    Channel(
        "Clubbing TV",
        "https://d1j2csarxnwazk.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-uze1m6xh4fiyr-ssai-prd/master.m3u8",
        category="music",
        language="en",
        country="global",
        tags=["dj", "electronic"]
    ),

    Channel(
        "Doctor Who Classic",
        "https://aegis-cloudfront-1.tubi.video/7e9ef0f5-4d13-4083-aa3f-9375e652a4c9/playlist.m3u8",
        category="entertainment",
        language="en",
        country="uk",
        tags=["series", "sci-fi"]
    ),

    Channel(
        "Create TV",
        "https://create.lls.pbs.org/index.m3u8",
        category="education",
        language="en",
        country="usa",
        tags=["diy", "cooking"]
    ),

    Channel(
        "Fox Weather",
        "https://247wlive.foxweather.com/stream/index.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["weather", "live"]
    ),

    Channel(
        "Fox News Radio (Live Video)",
        "https://radiovid.foxnews.com/hls/live/661547/RADIOVID/index.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["radio", "news"]
    ),

    Channel(
        "Entertainment Tonight (Mixible)",
        "https://cbsta49f-cbsta49f-ms.global.ssl.fastly.net/amagi7b98-AmagiMixible/master/amagi7b98-AmagiMixible.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["celebrity", "shows"]
    ),

    Channel(
        "FanDuel TV",
        "https://d2jl8r92tdc3f1.cloudfront.net/out/v1/59419700344b4625b7cb0693ba265ea3/TVGindex_1.m3u8",
        category="sports",
        language="en",
        country="usa",
        tags=["betting", "sports"]
    ),

    Channel(
        "FanDuel Racing",
        "https://d3ehq1uaxory6w.cloudfront.net/out/v1/35c05f080f4e49a4b4eb031b5a14e505/TVG2index_2.m3u8",
        category="sports",
        language="en",
        country="usa",
        tags=["horse racing"]
    ),

    Channel(
        "FilmRise Classic TV",
        "https://d2tv4k5moji5m7.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-lu4pzh9l4b57p/master.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["classic", "tv"]
    ),

    Channel(
        "Global Fashion Channel",
        "https://pubgfc.teleosmedia.com/linear/globalfashionchannel/globalfashionchannel/playlist.m3u8",
        category="entertainment",
        language="en",
        country="global",
        tags=["fashion", "lifestyle"]
    ),

    Channel(
        "Free Speech TV",
        "https://edge.fstv-live-linear-channel.top.comcast.net/Content/HLS_HLSv3/Live/channel(b168a609-19c1-2203-ae1d-6b9726f05e67)/index.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["politics", "talk"]
    ),

    Channel(
        "Duck Hunting TV",
        "https://main.duckhunting.playout.vju.tv/duckhuntingtv/main.m3u8",
        category="sports",
        language="en",
        country="usa",
        tags=["hunting", "outdoors"]
    ),

    Channel(
        "FNX (First Nations Experience)",
        "https://fnx.lls.pbs.org/index.m3u8",
        category="education",
        language="en",
        country="usa",
        tags=["culture", "indigenous"]
    ),

    Channel(
        "ION Plus",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg01438-ewscrippscompan-ionplus-tablo/playlist.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["series", "movies"]
    ),

    Channel(
        "Fox 4 Dallas (KDFW)",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00312-graytelevisioni-wbtvnews-vizious/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["local", "dallas"]
    ),

    Channel(
        "Grit Xtra",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg01438-ewscrippscompan-gritxtra-tablo/playlist.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["action", "westerns"]
    ),

    Channel(
        "HSN (Home Shopping Network)",
        "https://qvc-amd-live.akamaized.net/hls/live/2034113/lshsn1us/master.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["shopping"]
    ),

    Channel(
        "Jewelry Television",
        "https://content.jwplatform.com/live/broadcast/oe7UD7Ag.m3u8",
        category="entertainment",
        language="en",
        country="usa",
        tags=["shopping", "jewelry"]
    ),

    Channel(
        "InfoWars (Network Main)",
        "https://freespeech.akamaized.net/hls/live/2016712/live1/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["politics"]
    ),

    Channel(
        "History Hit",
        "https://amg00426-lds-amg00426c2-samsung-ph-4623.playouts.now.amagi.tv/playlist.m3u8",
        category="documentary",
        language="en",
        country="uk",
        tags=["history"]
    ),

    Channel(
        "Hope Channel North America",
        "https://jstre.am/live/jsl:0sUSK6VA7GT.m3u8",
        category="religion",
        language="en",
        country="usa",
        tags=["christian"]
    ),

    Channel(
        "It's Supernatural! Network (ISN)",
        "https://content.uplynk.com/channel/fbc0f835332e476397b12216f9042f78.m3u8",
        category="religion",
        language="en",
        country="usa",
        tags=["spiritual"]
    ),
    Channel(
        "LiveNOW from FOX",
        "https://fox-foxnewsnow-vizio.amagi.tv/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "live", "usa"]
    ),
    Channel(
        "NBC Los Angeles (KNBC)",
        "https://nbculocallive.akamaized.net/hls/live/2037084/losangeles/stream1/master.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "local", "los angeles"]
    ),
    Channel(
        "FOX 11 Los Angeles (KTTV)",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00488-foxdigital-fox11losangeleskttv-vizious/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "fox", "los angeles"]
    ),
    Channel(
        "FOX 9 Minneapolis (KMSP)",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00488-foxdigital-kmsp-lgus/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "fox", "minneapolis"]
    ),
    Channel(
        "KIRO 7 News Seattle",
        "https://cdn-ue1-prod.tsv2.amagi.tv/linear/amg00327-coxmediagroup-kirobreaking-ono/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "seattle"]
    ),
    Channel(
        "Lacrosse TV",
        "https://1840769862.rsc.cdn77.org/FTF/LSN_SCTE.m3u8",
        category="sports",
        language="en",
        country="international",
        tags=["sports", "lacrosse"]
    ),
    Channel(
        "LLBN His Light",
        "https://brightstar-hislight-pull-secure.akamaized.net/brightstarhislight/stream.m3u8",
        category="religion",
        language="en",
        country="usa",
        tags=["religion", "christian"]
    ),
    Channel(
        "LLBN Smart Life Style",
        "https://brightstar-sls-pull-secure.akamaized.net/brightstarsls/stream.m3u8",
        category="lifestyle",
        language="en",
        country="usa",
        tags=["lifestyle", "health"]
    ),
    Channel(
        "Lego Channel",
        "https://jmp2.uk/stvp-GBBC4300005AL",
        category="kids",
        language="en",
        country="international",
        tags=["kids", "lego"]
    ),
    Channel(
        "Newsmax TV",
        "https://nmx1ota.akamaized.net/hls/live/2107010/Live_1/index.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "politics"]
    ),
    Channel(
        "Newsmax 2",
        "https://nmxlive.akamaized.net/hls/live/529965/Live_1/index.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news"]
    ),
    Channel(
        "Mythbusters (Discovery)",
        "https://d1cgf0ptrv4t22.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-xvoparaodgcw9/Mythbusters_GB.m3u8",
        category="documentary",
        language="en",
        country="usa",
        tags=["science", "discovery"]
    ),
    Channel(
        "NBC San Diego (KNSD)",
        "https://nbculocallive.akamaized.net/hls/live/2037098/sandiego/stream1/master.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "san diego"]
    ),
    Channel(
        "NBCLX",
        "https://nbculocallive.akamaized.net/hls/live/2037096/lx/use1.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "nbc"]
    ),
    Channel(
        "NEW K-POP",
        "https://newidco-newkid-1-eu.xiaomi.wurl.tv/playlist.m3u8",
        category="music",
        language="ko",
        country="korea",
        tags=["music", "kpop"]
    ),
    Channel(
        "MotoAmerica TV",
        "https://1422977263.rsc.cdn77.org/HLS/MOTOAMERICA.m3u8",
        category="sports",
        language="en",
        country="usa",
        tags=["sports", "motor"]
    ),
    Channel(
        "MBC America",
        "https://cdn-us-east-prod-ingest-infra-dacast-com.akamaized.net/624ff8f9-db18-da92-4d42-896fa2ff3eb3/source/index.m3u8",
        category="general",
        language="en",
        country="usa",
        tags=["entertainment"]
    ),
    Channel(
        "LPTV (Lexington Media)",
        "https://livestream.telvue.com/lexmedia1/f7b44cfafd5c52223d5498196c8a2e7b.sdp/lexmedia1/stream1/playlist.m3u8",
        category="local",
        language="en",
        country="usa",
        tags=["local", "community"]
    ),
    Channel(
        "PBS Kids (National)",
        "https://livestream.pbskids.org/out/v1/14507d931bbe48a69287e4850e53443c/est.m3u8",
        category="kids",
        language="en",
        country="usa",
        tags=["kids", "education"]
    ),
    Channel(
        "Newsy (Scripps News)",
        "https://547f72e6652371c3.mediapackage.us-east-1.amazonaws.com/out/v1/e3e6e29095844c4ba7d887f01e44a5ef/index.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news"]
    ),

    Channel(
        "Fox 5 New York (WNYW)",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00488-foxdigital-wnyw-lgus/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "new york"]
    ),
    Channel(
        "Fox 5 Washington DC (WTTG)",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00488-foxdigital-fox5dcwttg-vizious/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "washington dc"]
    ),
    Channel(
        "Fox 2 Detroit (WJBK)",
        "https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00488-foxdigital-fox2detroitwjbk-vizious/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "detroit"]
    ),
    Channel(
        "Yahoo! Finance",
        "https://d1ewctnvcwvvvu.cloudfront.net/playlist.m3u8",
        category="business",
        language="en",
        country="usa",
        tags=["finance", "business", "stocks"]
    ),
    Channel(
        "World Channel (PBS)",
        "https://world.lls.pbs.org/index.m3u8",
        category="documentary",
        language="en",
        country="usa",
        tags=["pbs", "documentary"]
    ),
    Channel(
        "WSB-TV News (Atlanta)",
        "https://cdn-ue1-prod.tsv2.amagi.tv/linear/amg00327-coxmediagroup-wsbbreakingnews-ono/playlist.m3u8",
        category="news",
        language="en",
        country="usa",
        tags=["news", "atlanta"]
    ),
    Channel(
        "YTA TV (YouToo America)",
        "https://yta.unitedteleports.tv/hls/YTA.m3u8",
        category="general",
        language="en",
        country="usa",
        tags=["general"]
    ),
    Channel(
        "Drita TV",
        "https://dritatv.protokolldns.xyz/dritaweb5587989/index.m3u8",
        category="religion",
        language="sq",
        country="kosovo",
        tags=["religion", "islam"]
    ),
    Channel(
        "RTV Pendimi",
        "https://www.rtvpendimi.com:19360/tvpendimi/tvpendimi.m3u8",
        category="religion",
        language="sq",
        country="albania",
        tags=["religion"]
    ),
    Channel(
        "RTV Islam",
        "https://protokolldns.xyz/rtvislamweb554/index.m3u8",
        category="religion",
        language="sq",
        country="albania",
        tags=["islam"]
    ),
    Channel(
        "SRF 1 HD",
        "https://viamotionhsi.netplus.ch/live/eds/srf1hd/browser-HLS8/srf1hd.m3u8",
        category="general",
        language="de",
        country="switzerland",
        tags=["tv", "srf"]
    ),
    Channel(
        "SRF zwei HD",
        "https://viamotionhsi.netplus.ch/live/eds/srf2hd/browser-HLS8/srf2hd.m3u8",
        category="general",
        language="de",
        country="switzerland",
        tags=["tv"]
    ),
    Channel(
        "SRF info HD",
        "https://viamotionhsi.netplus.ch/live/eds/srfinfo/browser-HLS8/srfinfo.m3u8",
        category="news",
        language="de",
        country="switzerland",
        tags=["news"]
    ),
    Channel(
        "RTS 1 HD",
        "https://viamotionhsi.netplus.ch/live/eds/rts1hd/browser-HLS8/rts1hd.m3u8",
        category="general",
        language="fr",
        country="switzerland",
        tags=["tv"]
    ),
    Channel(
        "Leman Bleu",
        "https://viamotionhsi.netplus.ch/live/eds/lemanbleu/browser-HLS8/lemanbleu.m3u8",
        category="news",
        language="fr",
        country="switzerland",
        tags=["news", "local"]
    ),
    Channel(
        "TeleBielingue",
        "https://viamotionhsi.netplus.ch/live/eds/telebielingue/browser-HLS8/telebielingue.m3u8",
        category="news",
        language="de",
        country="switzerland",
        tags=["news", "local"]
    ),
    Channel(
        "TV 24 HD",
        "https://viamotionhsi.netplus.ch/live/eds/tv24/browser-HLS8/tv24.m3u8",
        category="general",
        language="de",
        country="switzerland",
        tags=["tv"]
    ),
    Channel(
        "Blue Zoom French",
        "https://viamotionhsi.netplus.ch/live/eds/bluezoomfr/browser-HLS8/bluezoomfr.m3u8",
        category="entertainment",
        language="fr",
        country="switzerland",
        tags=["entertainment"]
    ),
    Channel(
        "TVM3 (Music)",
        "https://livevideo.infomaniak.com/streaming/livecast/tvm3/playlist.m3u8",
        category="music",
        language="fr",
        country="switzerland",
        tags=["music"]
    ),
    Channel(
        "TeleZüri",
        "https://cdnapisec.kaltura.com/p/1719221/sp/171922100/playManifest/entryId/1_se36k3uk/protocol/https/format/applehttp/flavorIds/1_i4zc9zv3,1_2vzxm8zl,1_yjohpwzj/a.m3u8",
        category="news",
        language="de",
        country="switzerland",
        tags=["news", "zurich"]
    ),
    Channel(
        "TeleTicino (Italian)",
        "https://vstream-cdn.ch/hls/teleticino.m3u8",
        category="news",
        language="it",
        country="switzerland",
        tags=["news"]
    ),
    Channel(
        "TVO - Ostschweiz",
        "https://cdnapisec.kaltura.com/p/1719221/sp/171922100/playManifest/entryId/1_t5h46v64/format/applehttp/protocol/https/a.m3u8",
        category="news",
        language="de",
        country="switzerland",
        tags=["news"]
    ),
    Channel(
        "France 2 HD",
        "https://viamotionhsi.netplus.ch/live/eds/france2hd/browser-HLS8/france2hd.m3u8",
        category="general",
        language="fr",
        country="france",
        tags=["tv"]
    ),
    Channel(
        "France 5 HD",
        "https://viamotionhsi.netplus.ch/live/eds/france5hd/browser-HLS8/france5hd.m3u8",
        category="documentary",
        language="fr",
        country="france",
        tags=["documentary"]
    ),
    Channel(
        "BFM TV (News)",
        "https://viamotionhsi.netplus.ch/live/eds/bfmtv/browser-HLS8/bfmtv.m3u8",
        category="news",
        language="fr",
        country="france",
        tags=["news"]
    ),
    Channel(
        "CNews HD",
        "https://viamotionhsi.netplus.ch/live/eds/itele/browser-HLS8/itele.m3u8",
        category="news",
        language="fr",
        country="france",
        tags=["news"]
    ),
    Channel(
        "ADN TV+ (Anime)",
        "https://d3b73b34o7cvkq.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-gz2sgqzp076kf/adn.m3u8",
        category="anime",
        language="fr",
        country="france",
        tags=["anime"]
    ),
    Channel(
        "Caillou (Kids)",
        "https://do7nccdsswstc.cloudfront.net/v1/manifest/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-1aso0bc668saa/a5233c83-f772-4a81-959a-45ec7877ef61/5.m3u8",
        category="kids",
        language="en",
        country="international",
        tags=["kids"]
    ),
    Channel(
        "FashionTV Paris",
        "https://edge-fast3.evrideo.tv/bfdbb576-83f7-11f0-9f89-0200170e3e04_1000028043_HLS/manifest.m3u8",
        category="fashion",
        language="fr",
        country="france",
        tags=["fashion"]
    ),
    Channel(
        "Africanews English",
        "https://d35j504z0x2vu2.cloudfront.net/v1/master/0bc8e8376bd8417a1b6761138aa41c26c7309312/africanews/africanews-en.m3u8",
        category="news",
        language="en",
        country="africa",
        tags=["news"]
    ),
    Channel(
        "TF1 HD",
        "https://viamotionhsi.netplus.ch/live/eds/tf1hd/browser-HLS8/tf1hd.m3u8",
        category="general",
        language="fr",
        country="france",
        tags=["tv"]
    ),
    Channel(
        "M6 HD",
        "https://viamotionhsi.netplus.ch/live/eds/m6hd/browser-HLS8/m6hd.m3u8",
        category="general",
        language="fr",
        country="france",
        tags=["tv"]
    ),
    Channel(
        "W9",
        "https://viamotionhsi.netplus.ch/live/eds/w9/browser-HLS8/w9.m3u8",
        category="entertainment",
        language="fr",
        country="france",
        tags=["tv"]
    ),
    Channel(
        "Paramount Channel",
        "https://viamotionhsi.netplus.ch/live/eds/paramount/browser-HLS8/paramount.m3u8",
        category="entertainment",
        language="fr",
        country="france",
        tags=["movies"]
    ),
    Channel(
        "Planete+",
        "https://viamotionhsi.netplus.ch/live/eds/planeteplus/browser-HLS8/planeteplus.m3u8",
        category="documentary",
        language="fr",
        country="france",
        tags=["documentary"]
    ),
    Channel(
        "Game One",
        "https://viamotionhsi.netplus.ch/live/eds/gameone/browser-HLS8/gameone.m3u8",
        category="gaming",
        language="fr",
        country="france",
        tags=["gaming", "anime"]
    ),
    Channel(
        "L'Equipe HD",
        "https://dshn8inoshngm.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-gac2i63dmu8b7/LEquipe_FR.m3u8",
        category="sports",
        language="fr",
        country="france",
        tags=["sports"]
    ),
    Channel(
        "France 24 French",
        "https://live.france24.com/hls/live/2037179/F24_FR_HI_HLS/master_5000.m3u8",
        category="news",
        language="fr",
        country="france",
        tags=["news"]
    ),
    Channel(
        "BBC One HD",
        "https://november.queazified.co.uk/ee971134-115e-4418-8d1d-69dff7d4c6eb.m3u8",
        category="general",
        language="en",
        country="uk",
        tags=["tv"]
    ),
    Channel(
        "BBC Two HD",
        "https://viamotionhsi.netplus.ch/live/eds/bbc2/browser-HLS8/bbc2.m3u8",
        category="general",
        language="en",
        country="uk",
        tags=["tv"]
    ),
    Channel(
        "ITV 2 HD",
        "https://viamotionhsi.netplus.ch/live/eds/itv2/browser-HLS8/itv2.m3u8",
        category="entertainment",
        language="en",
        country="uk",
        tags=["tv"]
    ),
    Channel(
        "Channel 4 HD",
        "https://viamotionhsi.netplus.ch/live/eds/channel4/browser-HLS8/channel4.m3u8",
        category="entertainment",
        language="en",
        country="uk",
        tags=["tv"]
    ),
    Channel(
        "Sky Cinema Family HD",
        "https://d17lsiabqrlwa2.cloudfront.net/pl_138/207480-6535776-1/playlist.m3u8",
        category="movies",
        language="en",
        country="uk",
        tags=["movies"]
    ),
    Channel(
        "Film4 HD",
        "https://viamotionhsi.netplus.ch/live/eds/film4/browser-HLS8/film4.m3u8",
        category="movies",
        language="en",
        country="uk",
        tags=["movies"]
    ),
    Channel(
        "FIFA+ English",
        "https://a62dad94.wurl.com/master/f36d25e7e52f1ba8d7e56eb859c636563214f541/UmFrdXRlblRWLWV1X0ZJRkFQbHVzRW5nbGlzaF9ITFM/playlist.m3u8",
        category="sports",
        language="en",
        country="international",
        tags=["sports", "football"]
    ),
    Channel(
        "BBC News (International)",
        "https://viamotionhsi.netplus.ch/live/eds/bbcworld/browser-HLS8/bbcworld.m3u8",
        category="news",
        language="en",
        country="uk",
        tags=["news"]
    ),
    Channel(
        "Red Bull TV",
        "https://rbmn-live.akamaized.net/hls/live/590964/BoRB-AT/master.m3u8",
        category="sports",
        language="en",
        country="austria",
        tags=["sports", "extreme"]
    ),  

    Channel(
        "RTSH Shqip",
        "http://178.33.11.6:8696/live/rtshshqip/playlist.m3u8",
        category="news",
        language="sq",
        country="albania",
        tags=["albania", "balkan", "news"]
    ),

    Channel(
        "Euronews Albania",
        "https://gjirafa-video-live.gjirafa.net/gjvideo-live/2dw-zuf-1c9-pxu/index.m3u8",
        category="news",
        language="sq",
        country="albania",
        tags=["balkan", "europe"]
    ),

    Channel(
        "CBS Sports Golazo",
        "https://dai.google.com/linear/hls/event/GxrCGmwST0ixsrc_QgB6qw/master.m3u8",
        category="sports",
        language="en",
        country="usa",
        tags=["football", "soccer"]
    ),

    Channel(
        "KiKA",
        "https://kikahls.akamaized.net/hls/live/2022690/livetvkika_ww/master.m3u8",
        category="kids",
        language="de",
        country="germany",
        tags=["kids", "cartoons"]
    ),

    Channel(
        "PBS Kids",
        "https://livestream.pbskids.org/out/v1/14507d931bbe48a69287e4850e53443c/est.m3u8",
        category="kids",
        language="en",
        country="usa",
        tags=["kids", "education"]
    ),

    Channel(
        "Vevo Pop",
        "https://jmp2.uk/stvp-GBBC19000017V",
        category="music",
        language="en",
        country="global",
        tags=["music", "pop"]
    ),

    Channel(
        "Vevo Hip Hop",
        "https://d3mzlmrngyf08j.cloudfront.net/v1/master/cc-55k4m9whplndi/playlist.m3u8",
        category="music",
        language="en",
        country="global",
        tags=["music", "hiphop", "rap"]
    ),
]

def get_channels_by_category(category: str):
    return [ch for ch in CHANNELS if ch.category == category]


def search_channels_by_tag(keyword: str):
    keyword = keyword.lower()
    return [
        ch for ch in CHANNELS
        if ch.tags and any(keyword in tag for tag in ch.tags)
    ]


def get_news_channels():
    return get_channels_by_category("news")


def get_balkan_channels():
    return [
        ch for ch in CHANNELS
        if "balkan" in (ch.tags or [])
    ]


def find_best_channel(query: str):
    """
    Simple semantic matcher (upgrade point later to AI embeddings)
    """
    query = query.lower()

    best = None
    best_score = 0

    for ch in CHANNELS:
        score = 0

        if query in ch.name.lower():
            score += 5

        if ch.tags:
            for tag in ch.tags:
                if tag in query:
                    score += 3

        if ch.category in query:
            score += 2

        if score > best_score:
            best_score = score
            best = ch

    return best