! function() {
    "use strict";
    var i, catalog = {};
    function extname(t) {
        if (t.lastIndexOf(".") > 0) {
            return t.substr(t.lastIndexOf("."));
        } else {
            return "";
        }
    }
    i = {
        lookup: function(t) {
            return catalog[extname(t).toLowerCase()];
        },
        set: function(t, a) {
            return catalog[t] = a;
        }
    };
    var map = [
        [".ez", "application/andrew-inset"],
        [".aw", "application/applixware"],
        [".atom", "application/atom+xml"],
        [".atomcat", "application/atomcat+xml"],
        [".atomsvc", "application/atomsvc+xml"],
        [".ccxml", "application/ccxml+xml"],
        [".cu", "application/cu-seeme"],
        [".davmount", "application/davmount+xml"],
        [".ecma", "application/ecmascript"],
        [".emma", "application/emma+xml"],
        [".epub", "application/epub+zip"],
        [".pfr", "application/font-tdpfr"],
        [".stk", "application/hyperstudio"],
        [".jar", "application/java-archive"],
        [".ser", "application/java-serialized-object"],
        [".class", "application/java-vm"],
        [".js", "application/javascript"],
        [".json", "application/json"],
        [".lostxml", "application/lost+xml"],
        [".hqx", "application/mac-binhex40"],
        [".cpt", "application/mac-compactpro"],
        [".mrc", "application/marc"],
        [".ma,.nb,.mb", "application/mathematica"],
        [".mathml", "application/mathml+xml"],
        [".mbox", "application/mbox"],
        [".mscml", "application/mediaservercontrol+xml"],
        [".mp4s", "application/mp4"],
        [".doc,.dot", "application/msword"],
        [".mxf", "application/mxf"],
        [".oda", "application/oda"],
        [".opf", "application/oebps-package+xml"],
        [".ogx", "application/ogg"],
        [".onetoc,.onetoc2,.onetmp,.onepkg", "application/onenote"],
        [".xer", "application/patch-ops-error+xml"],
        [".pdf", "application/pdf"],
        [".pgp", "application/pgp-encrypted"],
        [".asc,.sig", "application/pgp-signature"],
        [".prf", "application/pics-rules"],
        [".p10", "application/pkcs10"],
        [".p7m,.p7c", "application/pkcs7-mime"],
        [".p7s", "application/pkcs7-signature"],
        [".cer", "application/pkix-cert"],
        [".crl", "application/pkix-crl"],
        [".pkipath", "application/pkix-pkipath"],
        [".pki", "application/pkixcmp"],
        [".pls", "application/pls+xml"],
        [".ai,.eps,.ps", "application/postscript"],
        [".cww", "application/prs.cww"],
        [".rdf", "application/rdf+xml"],
        [".rif", "application/reginfo+xml"],
        [".rnc", "application/relax-ng-compact-syntax"],
        [".rl", "application/resource-lists+xml"],
        [".rld", "application/resource-lists-diff+xml"],
        [".rs", "application/rls-services+xml"],
        [".rsd", "application/rsd+xml"],
        [".rss", "application/rss+xml"],
        [".rtf", "application/rtf"],
        [".sbml", "application/sbml+xml"],
        [".scq", "application/scvp-cv-request"],
        [".scs", "application/scvp-cv-response"],
        [".spq", "application/scvp-vp-request"],
        [".spp", "application/scvp-vp-response"],
        [".sdp", "application/sdp"],
        [".setpay", "application/set-payment-initiation"],
        [".setreg", "application/set-registration-initiation"],
        [".shf", "application/shf+xml"],
        [".smi,.smil", "application/smil+xml"],
        [".rq", "application/sparql-query"],
        [".srx", "application/sparql-results+xml"],
        [".gram", "application/srgs"],
        [".grxml", "application/srgs+xml"],
        [".ssml", "application/ssml+xml"],
        [".plb", "application/vnd.3gpp.pic-bw-large"],
        [".psb", "application/vnd.3gpp.pic-bw-small"],
        [".pvb", "application/vnd.3gpp.pic-bw-var"],
        [".tcap", "application/vnd.3gpp2.tcap"],
        [".pwn", "application/vnd.3m.post-it-notes"],
        [".aso", "application/vnd.accpac.simply.aso"],
        [".imp", "application/vnd.accpac.simply.imp"],
        [".acu", "application/vnd.acucobol"],
        [".atc,.acutc", "application/vnd.acucorp"],
        [".air", "application/vnd.adobe.air-application-installer-package+zip"],
        [".xdp", "application/vnd.adobe.xdp+xml"],
        [".xfdf", "application/vnd.adobe.xfdf"],
        [".azf", "application/vnd.airzip.filesecure.azf"],
        [".azs", "application/vnd.airzip.filesecure.azs"],
        [".azw", "application/vnd.amazon.ebook"],
        [".acc", "application/vnd.americandynamics.acc"],
        [".ami", "application/vnd.amiga.ami"],
        [".apk", "application/vnd.android.package-archive"],
        [".cii", "application/vnd.anser-web-certificate-issue-initiation"],
        [".fti", "application/vnd.anser-web-funds-transfer-initiation"],
        [".atx", "application/vnd.antix.game-component"],
        [".mpkg", "application/vnd.apple.installer+xml"],
        [".swi", "application/vnd.arastra.swi"],
        [".aep", "application/vnd.audiograph"],
        [".mpm", "application/vnd.blueice.multipass"],
        [".bmi", "application/vnd.bmi"],
        [".rep", "application/vnd.businessobjects"],
        [".cdxml", "application/vnd.chemdraw+xml"],
        [".mmd", "application/vnd.chipnuts.karaoke-mmd"],
        [".cdy", "application/vnd.cinderella"],
        [".cla", "application/vnd.claymore"],
        [".c4g,.c4d,.c4f,.c4p,.c4u", "application/vnd.clonk.c4group"],
        [".csp", "application/vnd.commonspace"],
        [".cdbcmsg", "application/vnd.contact.cmsg"],
        [".cmc", "application/vnd.cosmocaller"],
        [".clkx", "application/vnd.crick.clicker"],
        [".clkk", "application/vnd.crick.clicker.keyboard"],
        [".clkp", "application/vnd.crick.clicker.palette"],
        [".clkt", "application/vnd.crick.clicker.template"],
        [".clkw", "application/vnd.crick.clicker.wordbank"],
        [".wbs", "application/vnd.criticaltools.wbs+xml"],
        [".pml", "application/vnd.ctc-posml"],
        [".ppd", "application/vnd.cups-ppd"],
        [".car", "application/vnd.curl.car"],
        [".pcurl", "application/vnd.curl.pcurl"],
        [".rdz", "application/vnd.data-vision.rdz"],
        [".fe_launch", "application/vnd.denovo.fcselayout-link"],
        [".dna", "application/vnd.dna"],
        [".mlp", "application/vnd.dolby.mlp"],
        [".dpg", "application/vnd.dpgraph"],
        [".dfac", "application/vnd.dreamfactory"],
        [".geo", "application/vnd.dynageo"],
        [".mag", "application/vnd.ecowin.chart"],
        [".nml", "application/vnd.enliven"],
        [".esf", "application/vnd.epson.esf"],
        [".msf", "application/vnd.epson.msf"],
        [".qam", "application/vnd.epson.quickanime"],
        [".slt", "application/vnd.epson.salt"],
        [".ssf", "application/vnd.epson.ssf"],
        [".es3,.et3", "application/vnd.eszigno3+xml"],
        [".ez2", "application/vnd.ezpix-album"],
        [".ez3", "application/vnd.ezpix-package"],
        [".fdf", "application/vnd.fdf"],
        [".mseed", "application/vnd.fdsn.mseed"],
        [".seed,.dataless", "application/vnd.fdsn.seed"],
        [".gph", "application/vnd.flographit"],
        [".ftc", "application/vnd.fluxtime.clip"],
        [".fm,.frame,.maker,.book", "application/vnd.framemaker"],
        [".fnc", "application/vnd.frogans.fnc"],
        [".ltf", "application/vnd.frogans.ltf"],
        [".fsc", "application/vnd.fsc.weblaunch"],
        [".oas", "application/vnd.fujitsu.oasys"],
        [".oa2", "application/vnd.fujitsu.oasys2"],
        [".oa3", "application/vnd.fujitsu.oasys3"],
        [".fg5", "application/vnd.fujitsu.oasysgp"],
        [".bh2", "application/vnd.fujitsu.oasysprs"],
        [".ddd", "application/vnd.fujixerox.ddd"],
        [".xdw", "application/vnd.fujixerox.docuworks"],
        [".xbd", "application/vnd.fujixerox.docuworks.binder"],
        [".fzs", "application/vnd.fuzzysheet"],
        [".txd", "application/vnd.genomatix.tuxedo"],
        [".ggb", "application/vnd.geogebra.file"],
        [".ggt", "application/vnd.geogebra.tool"],
        [".gex,.gre", "application/vnd.geometry-explorer"],
        [".gmx", "application/vnd.gmx"],
        [".kml", "application/vnd.google-earth.kml+xml"],
        [".kmz", "application/vnd.google-earth.kmz"],
        [".gqf,.gqs", "application/vnd.grafeq"],
        [".gac", "application/vnd.groove-account"],
        [".ghf", "application/vnd.groove-help"],
        [".gim", "application/vnd.groove-identity-message"],
        [".grv", "application/vnd.groove-injector"],
        [".gtm", "application/vnd.groove-tool-message"],
        [".tpl", "application/vnd.groove-tool-template"],
        [".vcg", "application/vnd.groove-vcard"],
        [".zmm", "application/vnd.handheld-entertainment+xml"],
        [".hbci", "application/vnd.hbci"],
        [".les", "application/vnd.hhe.lesson-player"],
        [".hpgl", "application/vnd.hp-hpgl"],
        [".hpid", "application/vnd.hp-hpid"],
        [".hps", "application/vnd.hp-hps"],
        [".jlt", "application/vnd.hp-jlyt"],
        [".pcl", "application/vnd.hp-pcl"],
        [".pclxl", "application/vnd.hp-pclxl"],
        [".sfd-hdstx", "application/vnd.hydrostatix.sof-data"],
        [".x3d", "application/vnd.hzn-3d-crossword"],
        [".mpy", "application/vnd.ibm.minipay"],
        [".afp,.listafp,.list3820", "application/vnd.ibm.modcap"],
        [".irm", "application/vnd.ibm.rights-management"],
        [".sc", "application/vnd.ibm.secure-container"],
        [".icc,.icm", "application/vnd.iccprofile"],
        [".igl", "application/vnd.igloader"],
        [".ivp", "application/vnd.immervision-ivp"],
        [".ivu", "application/vnd.immervision-ivu"],
        [".xpw,.xpx", "application/vnd.intercon.formnet"],
        [".qbo", "application/vnd.intu.qbo"],
        [".qfx", "application/vnd.intu.qfx"],
        [".rcprofile", "application/vnd.ipunplugged.rcprofile"],
        [".irp", "application/vnd.irepository.package+xml"],
        [".xpr", "application/vnd.is-xpr"],
        [".jam", "application/vnd.jam"],
        [".rms", "application/vnd.jcp.javame.midlet-rms"],
        [".jisp", "application/vnd.jisp"],
        [".joda", "application/vnd.joost.joda-archive"],
        [".ktz,.ktr", "application/vnd.kahootz"],
        [".karbon", "application/vnd.kde.karbon"],
        [".chrt", "application/vnd.kde.kchart"],
        [".kfo", "application/vnd.kde.kformula"],
        [".flw", "application/vnd.kde.kivio"],
        [".kon", "application/vnd.kde.kontour"],
        [".kpr,.kpt", "application/vnd.kde.kpresenter"],
        [".ksp", "application/vnd.kde.kspread"],
        [".kwd,.kwt", "application/vnd.kde.kword"],
        [".htke", "application/vnd.kenameaapp"],
        [".kia", "application/vnd.kidspiration"],
        [".kne,.knp", "application/vnd.kinar"],
        [".skp,.skd,.skt,.skm", "application/vnd.koan"],
        [".sse", "application/vnd.kodak-descriptor"],
        [".lbd", "application/vnd.llamagraphics.life-balance.desktop"],
        [".lbe", "application/vnd.llamagraphics.life-balance.exchange+xml"],
        [".123", "application/vnd.lotus-1-2-3"],
        [".apr", "application/vnd.lotus-approach"],
        [".pre", "application/vnd.lotus-freelance"],
        [".nsf", "application/vnd.lotus-notes"],
        [".org", "application/vnd.lotus-organizer"],
        [".scm", "application/vnd.lotus-screencam"],
        [".lwp", "application/vnd.lotus-wordpro"],
        [".portpkg", "application/vnd.macports.portpkg"],
        [".mcd", "application/vnd.mcd"],
        [".mc1", "application/vnd.medcalcdata"],
        [".cdkey", "application/vnd.mediastation.cdkey"],
        [".mwf", "application/vnd.mfer"],
        [".mfm", "application/vnd.mfmp"],
        [".flo", "application/vnd.micrografx.flo"],
        [".igx", "application/vnd.micrografx.igx"],
        [".mif", "application/vnd.mif"],
        [".daf", "application/vnd.mobius.daf"],
        [".dis", "application/vnd.mobius.dis"],
        [".mbk", "application/vnd.mobius.mbk"],
        [".mqy", "application/vnd.mobius.mqy"],
        [".msl", "application/vnd.mobius.msl"],
        [".plc", "application/vnd.mobius.plc"],
        [".txf", "application/vnd.mobius.txf"],
        [".mpn", "application/vnd.mophun.application"],
        [".mpc", "application/vnd.mophun.certificate"],
        [".xul", "application/vnd.mozilla.xul+xml"],
        [".cil", "application/vnd.ms-artgalry"],
        [".cab", "application/vnd.ms-cab-compressed"],
        [".xls,.xlm,.xla,.xlc,.xlt,.xlw", "application/vnd.ms-excel"],
        [".xlam", "application/vnd.ms-excel.addin.macroenabled.12"],
        [".xlsb", "application/vnd.ms-excel.sheet.binary.macroenabled.12"],
        [".xlsm", "application/vnd.ms-excel.sheet.macroenabled.12"],
        [".xltm", "application/vnd.ms-excel.template.macroenabled.12"],
        [".eot", "application/vnd.ms-fontobject"],
        [".chm", "application/vnd.ms-htmlhelp"],
        [".ims", "application/vnd.ms-ims"],
        [".lrm", "application/vnd.ms-lrm"],
        [".cat", "application/vnd.ms-pki.seccat"],
        [".stl", "application/vnd.ms-pki.stl"],
        [".ppt,.pps,.pot", "application/vnd.ms-powerpoint"],
        [".ppam", "application/vnd.ms-powerpoint.addin.macroenabled.12"],
        [".pptm", "application/vnd.ms-powerpoint.presentation.macroenabled.12"],
        [".sldm", "application/vnd.ms-powerpoint.slide.macroenabled.12"],
        [".ppsm", "application/vnd.ms-powerpoint.slideshow.macroenabled.12"],
        [".potm", "application/vnd.ms-powerpoint.template.macroenabled.12"],
        [".mpp,.mpt", "application/vnd.ms-project"],
        [".docm", "application/vnd.ms-word.document.macroenabled.12"],
        [".dotm", "application/vnd.ms-word.template.macroenabled.12"],
        [".wps,.wks,.wcm,.wdb", "application/vnd.ms-works"],
        [".wpl", "application/vnd.ms-wpl"],
        [".xps", "application/vnd.ms-xpsdocument"],
        [".mseq", "application/vnd.mseq"],
        [".mus", "application/vnd.musician"],
        [".msty", "application/vnd.muvee.style"],
        [".nlu", "application/vnd.neurolanguage.nlu"],
        [".nnd", "application/vnd.noblenet-directory"],
        [".nns", "application/vnd.noblenet-sealer"],
        [".nnw", "application/vnd.noblenet-web"],
        [".ngdat", "application/vnd.nokia.n-gage.data"],
        [".n-gage", "application/vnd.nokia.n-gage.symbian.install"],
        [".rpst", "application/vnd.nokia.radio-preset"],
        [".rpss", "application/vnd.nokia.radio-presets"],
        [".edm", "application/vnd.novadigm.edm"],
        [".edx", "application/vnd.novadigm.edx"],
        [".ext", "application/vnd.novadigm.ext"],
        [".odc", "application/vnd.oasis.opendocument.chart"],
        [".otc", "application/vnd.oasis.opendocument.chart-template"],
        [".odb", "application/vnd.oasis.opendocument.database"],
        [".odf", "application/vnd.oasis.opendocument.formula"],
        [".odft", "application/vnd.oasis.opendocument.formula-template"],
        [".odg", "application/vnd.oasis.opendocument.graphics"],
        [".otg", "application/vnd.oasis.opendocument.graphics-template"],
        [".odi", "application/vnd.oasis.opendocument.image"],
        [".oti", "application/vnd.oasis.opendocument.image-template"],
        [".odp", "application/vnd.oasis.opendocument.presentation"],
        [".ods", "application/vnd.oasis.opendocument.spreadsheet"],
        [".ots", "application/vnd.oasis.opendocument.spreadsheet-template"],
        [".odt", "application/vnd.oasis.opendocument.text"],
        [".otm", "application/vnd.oasis.opendocument.text-master"],
        [".ott", "application/vnd.oasis.opendocument.text-template"],
        [".oth", "application/vnd.oasis.opendocument.text-web"],
        [".xo", "application/vnd.olpc-sugar"],
        [".dd2", "application/vnd.oma.dd2+xml"],
        [".oxt", "application/vnd.openofficeorg.extension"],
        [".pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"],
        [".sldx", "application/vnd.openxmlformats-officedocument.presentationml.slide"],
        [".ppsx", "application/vnd.openxmlformats-officedocument.presentationml.slideshow"],
        [".potx", "application/vnd.openxmlformats-officedocument.presentationml.template"],
        [".xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        [".xltx", "application/vnd.openxmlformats-officedocument.spreadsheetml.template"],
        [".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
        [".dotx", "application/vnd.openxmlformats-officedocument.wordprocessingml.template"],
        [".dp", "application/vnd.osgi.dp"],
        [".pdb,.pqa,.oprc", "application/vnd.palm"],
        [".str", "application/vnd.pg.format"],
        [".ei6", "application/vnd.pg.osasli"],
        [".efif", "application/vnd.picsel"],
        [".plf", "application/vnd.pocketlearn"],
        [".pbd", "application/vnd.powerbuilder6"],
        [".box", "application/vnd.previewsystems.box"],
        [".mgz", "application/vnd.proteus.magazine"],
        [".qps", "application/vnd.publishare-delta-tree"],
        [".ptid", "application/vnd.pvi.ptid1"],
        [".qxd,.qxt,.qwd,.qwt,.qxl,.qxb", "application/vnd.quark.quarkxpress"],
        [".mxl", "application/vnd.recordare.musicxml"],
        [".musicxml", "application/vnd.recordare.musicxml+xml"],
        [".cod", "application/vnd.rim.cod"],
        [".rm", "application/vnd.rn-realmedia"],
        [".link66", "application/vnd.route66.link66+xml"],
        [".see", "application/vnd.seemail"],
        [".sema", "application/vnd.sema"],
        [".semd", "application/vnd.semd"],
        [".semf", "application/vnd.semf"],
        [".ifm", "application/vnd.shana.informed.formdata"],
        [".itp", "application/vnd.shana.informed.formtemplate"],
        [".iif", "application/vnd.shana.informed.interchange"],
        [".ipk", "application/vnd.shana.informed.package"],
        [".twd,.twds", "application/vnd.simtech-mindmapper"],
        [".mmf", "application/vnd.smaf"],
        [".teacher", "application/vnd.smart.teacher"],
        [".sdkm,.sdkd", "application/vnd.solent.sdkm+xml"],
        [".dxp", "application/vnd.spotfire.dxp"],
        [".sfs", "application/vnd.spotfire.sfs"],
        [".sdc", "application/vnd.stardivision.calc"],
        [".sda", "application/vnd.stardivision.draw"],
        [".sdd", "application/vnd.stardivision.impress"],
        [".smf", "application/vnd.stardivision.math"],
        [".sdw", "application/vnd.stardivision.writer"],
        [".vor", "application/vnd.stardivision.writer"],
        [".sgl", "application/vnd.stardivision.writer-global"],
        [".sxc", "application/vnd.sun.xml.calc"],
        [".stc", "application/vnd.sun.xml.calc.template"],
        [".sxd", "application/vnd.sun.xml.draw"],
        [".std", "application/vnd.sun.xml.draw.template"],
        [".sxi", "application/vnd.sun.xml.impress"],
        [".sti", "application/vnd.sun.xml.impress.template"],
        [".sxm", "application/vnd.sun.xml.math"],
        [".sxw", "application/vnd.sun.xml.writer"],
        [".sxg", "application/vnd.sun.xml.writer.global"],
        [".stw", "application/vnd.sun.xml.writer.template"],
        [".sus,.susp", "application/vnd.sus-calendar"],
        [".svd", "application/vnd.svd"],
        [".sis,.sisx", "application/vnd.symbian.install"],
        [".xsm", "application/vnd.syncml+xml"],
        [".bdm", "application/vnd.syncml.dm+wbxml"],
        [".xdm", "application/vnd.syncml.dm+xml"],
        [".tao", "application/vnd.tao.intent-module-archive"],
        [".tmo", "application/vnd.tmobile-livetv"],
        [".tpt", "application/vnd.trid.tpt"],
        [".mxs", "application/vnd.triscape.mxs"],
        [".tra", "application/vnd.trueapp"],
        [".ufd,.ufdl", "application/vnd.ufdl"],
        [".utz", "application/vnd.uiq.theme"],
        [".umj", "application/vnd.umajin"],
        [".unityweb", "application/vnd.unity"],
        [".uoml", "application/vnd.uoml+xml"],
        [".vcx", "application/vnd.vcx"],
        [".vsd,.vst,.vss,.vsw", "application/vnd.visio"],
        [".vis", "application/vnd.visionary"],
        [".vsf", "application/vnd.vsf"],
        [".wbxml", "application/vnd.wap.wbxml"],
        [".wmlc", "application/vnd.wap.wmlc"],
        [".wmlsc", "application/vnd.wap.wmlscriptc"],
        [".wtb", "application/vnd.webturbo"],
        [".wpd", "application/vnd.wordperfect"],
        [".wqd", "application/vnd.wqd"],
        [".stf", "application/vnd.wt.stf"],
        [".xar", "application/vnd.xara"],
        [".xfdl", "application/vnd.xfdl"],
        [".hvd", "application/vnd.yamaha.hv-dic"],
        [".hvs", "application/vnd.yamaha.hv-script"],
        [".hvp", "application/vnd.yamaha.hv-voice"],
        [".osf", "application/vnd.yamaha.openscoreformat"],
        [".osfpvg", "application/vnd.yamaha.openscoreformat.osfpvg+xml"],
        [".saf", "application/vnd.yamaha.smaf-audio"],
        [".spf", "application/vnd.yamaha.smaf-phrase"],
        [".cmp", "application/vnd.yellowriver-custom-menu"],
        [".zir,.zirz", "application/vnd.zul"],
        [".zaz", "application/vnd.zzazz.deck+xml"],
        [".vxml", "application/voicexml+xml"],
        [".hlp", "application/winhlp"],
        [".wsdl", "application/wsdl+xml"],
        [".wspolicy", "application/wspolicy+xml"],
        [".abw", "application/x-abiword"],
        [".ace", "application/x-ace-compressed"],
        [".aab,.x32,.u32,.vox", "application/x-authorware-bin"],
        [".aam", "application/x-authorware-map"],
        [".aas", "application/x-authorware-seg"],
        [".bcpio", "application/x-bcpio"],
        [".torrent", "application/x-bittorrent"],
        [".bz", "application/x-bzip"],
        [".bz2,.boz", "application/x-bzip2"],
        [".vcd", "application/x-cdlink"],
        [".chat", "application/x-chat"],
        [".pgn", "application/x-chess-pgn"],
        [".cpio", "application/x-cpio"],
        [".csh", "application/x-csh"],
        [".deb,.udeb", "application/x-debian-package"],
        [".dir,.dcr,.dxr,.cst,.cct,.cxt,.w3d,.fgd,.swa", "application/x-director"],
        [".wad", "application/x-doom"],
        [".ncx", "application/x-dtbncx+xml"],
        [".dtb", "application/x-dtbook+xml"],
        [".res", "application/x-dtbresource+xml"],
        [".dvi", "application/x-dvi"],
        [".bdf", "application/x-font-bdf"],
        [".gsf", "application/x-font-ghostscript"],
        [".psf", "application/x-font-linux-psf"],
        [".otf", "application/x-font-otf"],
        [".pcf", "application/x-font-pcf"],
        [".snf", "application/x-font-snf"],
        [".ttf,.ttc", "application/x-font-ttf"],
        [".woff", "application/font-woff"],
        [".pfa,.pfb,.pfm,.afm", "application/x-font-type1"],
        [".spl", "application/x-futuresplash"],
        [".gnumeric", "application/x-gnumeric"],
        [".gtar", "application/x-gtar"],
        [".hdf", "application/x-hdf"],
        [".jnlp", "application/x-java-jnlp-file"],
        [".latex", "application/x-latex"],
        [".prc,.mobi", "application/x-mobipocket-ebook"],
        [".application", "application/x-ms-application"],
        [".wmd", "application/x-ms-wmd"],
        [".wmz", "application/x-ms-wmz"],
        [".xbap", "application/x-ms-xbap"],
        [".mdb", "application/x-msaccess"],
        [".obd", "application/x-msbinder"],
        [".crd", "application/x-mscardfile"],
        [".clp", "application/x-msclip"],
        [".exe,.dll,.com,.bat,.msi", "application/x-msdownload"],
        [".mvb,.m13,.m14", "application/x-msmediaview"],
        [".wmf", "application/x-msmetafile"],
        [".mny", "application/x-msmoney"],
        [".pub", "application/x-mspublisher"],
        [".scd", "application/x-msschedule"],
        [".trm", "application/x-msterminal"],
        [".wri", "application/x-mswrite"],
        [".nc,.cdf", "application/x-netcdf"],
        [".p12,.pfx", "application/x-pkcs12"],
        [".p7b,.spc", "application/x-pkcs7-certificates"],
        [".p7r", "application/x-pkcs7-certreqresp"],
        [".rar", "application/x-rar-compressed"],
        [".sh", "application/x-sh"],
        [".shar", "application/x-shar"],
        [".swf", "application/x-shockwave-flash"],
        [".xap", "application/x-silverlight-app"],
        [".sit", "application/x-stuffit"],
        [".sitx", "application/x-stuffitx"],
        [".sv4cpio", "application/x-sv4cpio"],
        [".sv4crc", "application/x-sv4crc"],
        [".tar", "application/x-tar"],
        [".tcl", "application/x-tcl"],
        [".tex", "application/x-tex"],
        [".tfm", "application/x-tex-tfm"],
        [".texinfo,.texi", "application/x-texinfo"],
        [".ustar", "application/x-ustar"],
        [".src", "application/x-wais-source"],
        [".der,.crt", "application/x-x509-ca-cert"],
        [".fig", "application/x-xfig"],
        [".xpi", "application/x-xpinstall"],
        [".xenc", "application/xenc+xml"],
        [".xhtml,.xht", "application/xhtml+xml"],
        [".xml,.xsl", "application/xml"],
        [".dtd", "application/xml-dtd"],
        [".xop", "application/xop+xml"],
        [".xslt", "application/xslt+xml"],
        [".xspf", "application/xspf+xml"],
        [".mxml,.xhvml,.xvml,.xvm", "application/xv+xml"],
        [".zip", "application/zip"],
        [".adp", "audio/adpcm"],
        [".au,.snd", "audio/basic"],
        [".mid,.midi,.kar,.rmi", "audio/midi"],
        [".mp4a", "audio/mp4"],
        [".m4a,.m4p", "audio/mp4a-latm"],
        [".mpga,.mp2,.mp2a,.mp3,.m2a,.m3a", "audio/mpeg"],
        [".oga,.ogg,.spx", "audio/ogg"],
        [".eol", "audio/vnd.digital-winds"],
        [".dts", "audio/vnd.dts"],
        [".dtshd", "audio/vnd.dts.hd"],
        [".lvp", "audio/vnd.lucent.voice"],
        [".pya", "audio/vnd.ms-playready.media.pya"],
        [".ecelp4800", "audio/vnd.nuera.ecelp4800"],
        [".ecelp7470", "audio/vnd.nuera.ecelp7470"],
        [".ecelp9600", "audio/vnd.nuera.ecelp9600"],
        [".aac", "audio/x-aac"],
        [".aif,.aiff,.aifc", "audio/x-aiff"],
        [".m3u", "audio/x-mpegurl"],
        [".wax", "audio/x-ms-wax"],
        [".wma", "audio/x-ms-wma"],
        [".ram,.ra", "audio/x-pn-realaudio"],
        [".rmp", "audio/x-pn-realaudio-plugin"],
        [".wav", "audio/x-wav"],
        [".cdx", "chemical/x-cdx"],
        [".cif", "chemical/x-cif"],
        [".cmdf", "chemical/x-cmdf"],
        [".cml", "chemical/x-cml"],
        [".csml", "chemical/x-csml"],
        [".xyz", "chemical/x-xyz"],
        [".bmp", "image/bmp"],
        [".cgm", "image/cgm"],
        [".g3", "image/g3fax"],
        [".gif", "image/gif"],
        [".ief", "image/ief"],
        [".jp2", "image/jp2"],
        [".jpeg,.jpg,.jpe", "image/jpeg"],
        [".pict,.pic,.pct", "image/pict"],
        [".png", "image/png"],
        [".btif", "image/prs.btif"],
        [".svg,.svgz", "image/svg+xml"],
        [".tiff,.tif", "image/tiff"],
        [".psd", "image/vnd.adobe.photoshop"],
        [".djvu,.djv", "image/vnd.djvu"],
        [".dwg", "image/vnd.dwg"],
        [".dxf", "image/vnd.dxf"],
        [".fbs", "image/vnd.fastbidsheet"],
        [".fpx", "image/vnd.fpx"],
        [".fst", "image/vnd.fst"],
        [".mmr", "image/vnd.fujixerox.edmics-mmr"],
        [".rlc", "image/vnd.fujixerox.edmics-rlc"],
        [".mdi", "image/vnd.ms-modi"],
        [".npx", "image/vnd.net-fpx"],
        [".wbmp", "image/vnd.wap.wbmp"],
        [".xif", "image/vnd.xiff"],
        [".ras", "image/x-cmu-raster"],
        [".cmx", "image/x-cmx"],
        [".fh,.fhc,.fh4,.fh5,.fh7", "image/x-freehand"],
        [".ico", "image/x-icon"],
        [".pntg,.pnt,.mac", "image/x-macpaint"],
        [".pcx", "image/x-pcx"],
        [".pnm", "image/x-portable-anymap"],
        [".pbm", "image/x-portable-bitmap"],
        [".pgm", "image/x-portable-graymap"],
        [".ppm", "image/x-portable-pixmap"],
        [".qtif,.qti", "image/x-quicktime"],
        [".rgb", "image/x-rgb"],
        [".xbm", "image/x-xbitmap"],
        [".xpm", "image/x-xpixmap"],
        [".xwd", "image/x-xwindowdump"],
        [".eml,.mime", "message/rfc822"],
        [".igs,.iges", "model/iges"],
        [".msh,.mesh,.silo", "model/mesh"],
        [".dwf", "model/vnd.dwf"],
        [".gdl", "model/vnd.gdl"],
        [".gtw", "model/vnd.gtw"],
        [".mts", "model/vnd.mts"],
        [".vtu", "model/vnd.vtu"],
        [".wrl,.vrml", "model/vrml"],
        [".ics,.ifb", "text/calendar"],
        [".css", "text/css"],
        [".csv", "text/csv"],
        [".html,.htm", "text/html"],
        [".txt,.text,.conf,.def,.list,.log,.in", "text/plain"],
        [".dsc", "text/prs.lines.tag"],
        [".rtx", "text/richtext"],
        [".sgml,.sgm", "text/sgml"],
        [".tsv", "text/tab-separated-values"],
        [".t,.tr,.roff,.man,.me,.ms", "text/troff"],
        [".uri,.uris,.urls", "text/uri-list"],
        [".curl", "text/vnd.curl"],
        [".dcurl", "text/vnd.curl.dcurl"],
        [".scurl", "text/vnd.curl.scurl"],
        [".mcurl", "text/vnd.curl.mcurl"],
        [".fly", "text/vnd.fly"],
        [".flx", "text/vnd.fmi.flexstor"],
        [".gv", "text/vnd.graphviz"],
        [".3dml", "text/vnd.in3d.3dml"],
        [".spot", "text/vnd.in3d.spot"],
        [".jad", "text/vnd.sun.j2me.app-descriptor"],
        [".wml", "text/vnd.wap.wml"],
        [".wmls", "text/vnd.wap.wmlscript"],
        [".s,.asm", "text/x-asm"],
        [".c,.cc,.cxx,.cpp,.h,.hh,.dic", "text/x-c"],
        [".f,.for,.f77,.f90", "text/x-fortran"],
        [".p,.pas", "text/x-pascal"],
        [".java", "text/x-java-source"],
        [".etx", "text/x-setext"],
        [".uu", "text/x-uuencode"],
        [".vcs", "text/x-vcalendar"],
        [".vcf", "text/x-vcard"],
        [".3gp", "video/3gpp"],
        [".3g2", "video/3gpp2"],
        [".h261", "video/h261"],
        [".h263", "video/h263"],
        [".h264", "video/h264"],
        [".jpgv", "video/jpeg"],
        [".jpm,.jpgm", "video/jpm"],
        [".mj2,.mjp2", "video/mj2"],
        [".mp4,.mp4v,.mpg4,.m4v", "video/mp4"],
        [".mkv,.mk3d,.mka,.mks", "video/x-matroska"],
        [".webm", "video/webm"],
        [".mpeg,.mpg,.mpe,.m1v,.m2v", "video/mpeg"],
        [".ogv", "video/ogg"],
        [".qt,.mov", "video/quicktime"],
        [".fvt", "video/vnd.fvt"],
        [".mxu,.m4u", "video/vnd.mpegurl"],
        [".pyv", "video/vnd.ms-playready.media.pyv"],
        [".viv", "video/vnd.vivo"],
        [".dv,.dif", "video/x-dv"],
        [".f4v", "video/x-f4v"],
        [".fli", "video/x-fli"],
        [".flv", "video/x-flv"],
        [".asf,.asx", "video/x-ms-asf"],
        [".wm", "video/x-ms-wm"],
        [".wmv", "video/x-ms-wmv"],
        [".wmx", "video/x-ms-wmx"],
        [".wvx", "video/x-ms-wvx"],
        [".avi", "video/x-msvideo"],
        [".movie", "video/x-sgi-movie"],
        [".ice", "x-conference/x-cooltalk"],
        [".indd", "application/x-indesign"],
        [".dat", "application/octet-stream"],
        [".gz", "application/x-gzip"],
        [".tgz", "application/x-tar"],
        [".tar", "application/x-tar"],
        [".epub", "application/epub+zip"],
        [".mobi", "application/x-mobipocket-ebook"],
        ["README,LICENSE,COPYING,TODO,ABOUT,AUTHORS,CONTRIBUTORS", "text/plain"],
        ["manifest,.manifest,.mf,.appcache", "text/cache-manifest"]
    ];
    for(var j=0;j<map.length;j++){
        var l = map[j][0].split(",");
        for (var k=0;k<l.length;k++) {
            i.set(l[k], map[j][1]);
        }
    }
    map = null;
    window.mimeType = i;
}();
!function() {
    var hasTouchScreen = false;
    if ("maxTouchPoints" in navigator) {
        hasTouchScreen = navigator.maxTouchPoints > 0;
    } else if ("msMaxTouchPoints" in navigator) {
        hasTouchScreen = navigator.msMaxTouchPoints > 0;
    } else {
        var mQ = window.matchMedia && matchMedia("(pointer:coarse)");
        if (mQ && mQ.media === "(pointer:coarse)") {
            hasTouchScreen = !!mQ.matches;
        } else if ('orientation' in window) {
            hasTouchScreen = true;
        } else {
            var UA = navigator.userAgent;
            hasTouchScreen = (
                /\b(BlackBerry|webOS|iPhone|IEMobile)\b/i.test(UA) ||
                /\b(Android|Windows Phone|iPad|iPod)\b/i.test(UA)
            );
        }
    }
    window.is_mobile = hasTouchScreen;
}();
function hash(blob, hash_flags, cbProgress) {
    function readChunked(file, hash_flags, chunkCallback, endCallback) {
        var fileSize = file.size;
        var chunkSize = 50*1024*1024;
        var offset = 0;
        var reader = new FileReader();
        reader.onload = function () {
            if (reader.error) {
                endCallback(reader.error || {});
                return;
            }
            if (hash_flags["abort"]){
                endCallback({});
                return;
            }
            offset += reader.result.length;
            try {
                chunkCallback(reader.result, offset, fileSize);
            }
            catch (e){
                endCallback(e);
                return;
            }
            if (offset >= fileSize) {
                endCallback(null);
                fileSize = chunkSize = offset = reader = null;
                return;
            }
            readNext();
        };
        reader.onerror = function (err) {
            endCallback(err || {});
        };
        function readNext() {
            var fileSlice = file.slice(offset, offset+chunkSize);
            reader.readAsBinaryString(fileSlice);
            fileSlice = null;
        }
        readNext();
    }
    return new Promise(function(resolve, reject) {
        var sha256 = CryptoJS.algo.SHA256.create();
        readChunked(blob, hash_flags, function(chunk, offs, total) {
            sha256.update(CryptoJS.enc.Latin1.parse(chunk));
            typeof cbProgress === "function" && cbProgress(offs / total);
        }, function(err) {
            if (err) {
                reject(err);
            } else {
                try{
                    resolve(sha256.finalize().toString(CryptoJS.enc.Hex));
                    err = sha256 = blob = cbProgress = null;
                }
                catch (e){
                    reject(e);
                    e = err = sha256 = blob = cbProgress = null;
                }
            }
        });
    });
}
function setup_popup_select(){
    $("div#popup_select").on("click", function () {
        $("div#select_options").empty();
        $(this).removeClass("show");
    }).find("div#select_content").on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
    });
    $("select").each(function () {
        var _this = $(this);
        $(this).css({"pointer-events": "none"}).parent().css({"cursor": "pointer"}).off("click").on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            $("div#select_title h2").html(_this.data("title"));
            var options = $(this).find("option");
            var has_depth = options.is("[data-depth]");
            options = options.map(function (i, e) {
                e = $(e);
                var depth = parseInt(e.data("depth"))||0;
                var html = e.html().replace(/^　+/g, "");
                var _i = html.indexOf(" ");
                html = [html.slice(0, _i), html.slice(_i+1)];
                html[0] = "<span"+(has_depth?" class='collapsed'":"")+">"+html[0]+"</span>";
                html = html.join(" ");
                return "<div "+(has_depth&&depth?" style='display:none'":"")+"class='depth"+depth+"' data-val='"+e.attr("value")+"' data-name='"+e.data("name")+"'>"+html+"</div>";
            }).get().join("");
            options = $("div#popup_select").addClass("show").find("div#select_options").html(options);
            options.children().on("click", function () {
                _this.val($(this).data("val"));
                $("div#popup_select").trigger("click");
            }).find("span").on("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                if($(this).hasClass("disabled")){
                    return;
                }
                var cdepth = parseInt($(this).parent().attr("class").split("depth").slice(-1)[0]);
                if($(this).hasClass("collapsed")){
                    $(this).removeClass("collapsed");
                    $(this).parent().nextAll().each(function(i,e){
                        e=$(e);
                        var depth = parseInt(e.attr("class").split("depth").slice(-1)[0]);
                        if(depth<=cdepth) {
                            return false;
                        }
                        if(cdepth+1===depth) {
                            e.slideDown().find("span").addClass("collapsed");
                        }
                    }).end();
                }
                else {
                    $(this).addClass("collapsed");
                    $(this).parent().nextAll(":visible").each(function(i,e){
                        e=$(e);
                        var depth = parseInt(e.attr("class").split("depth").slice(-1)[0]);
                        if(depth<=cdepth) {
                            return false;
                        }
                        e.slideUp().find("span").addClass("collapsed");
                    }).end();
                }
            }).each(function () {
                var cdepth = parseInt($(this).parent().attr("class").split("depth").slice(-1)[0]);
                try{
                    var ndepth = parseInt($(this).parent().next().attr("class").split("depth").slice(-1)[0]);
                    if(cdepth>=ndepth){
                        $(this).addClass("disabled");
                    }
                }
                catch (e) {
                    $(this).addClass("disabled");
                }
            });
            var search_to;
            options.parent().find("div#select_search input").val("").off("keyup").on("keyup", function () {
                clearTimeout(search_to);
                var _this = $(this);
                if(!_this.val()){
                    options.children().removeClass("hide show");
                    return;
                }
                search_to = setTimeout(function (){
                    try{
                        var regex = new RegExp().compile(_this.val());
                    }
                    catch (e){
                        var regex = _this.val();
                    }
                    options.children().each(function () {
                        $(this).addClass("hide");
                        if(regex instanceof RegExp){
                            if(regex.test($(this).data("name").toString())){
                                $(this).addClass("show");
                            }
                        }
                        else{
                            if($(this).data("name").toString().indexOf(regex)!==-1){
                                $(this).addClass("show");
                            }
                        }
                    });
                }, 1000);
            });
        });
    });
}
function gen_randstr(){
    var s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    return Array(32).join().split(",").map(function() { return s.charAt(Math.floor(Math.random() * s.length)); }).join("");
}
function update_title_hints(){
    $("div.title_hint").remove();
    function trigger() {
        var id = "_"+gen_randstr().toLowerCase();
        $(this).attr("data-id", id);
        var title_hint = $("<div class='title_hint"+(is_mobile?" mobile":"")+"' "+id+" />").appendTo("body");
        var _this = $(this);
        var offset = _this.offset();
        title_hint.html($(this).data("title"));
        offset = {
            "top": offset.top+_this.outerHeight(),
            "left": offset.left-((title_hint.outerWidth()-_this.outerWidth())/2)
        };
        if (offset.left<$(document).outerWidth()*.1){
            title_hint.append("<style>div.title_hint["+id+"]:after{left:calc(50% + "+(offset.left-$(document).outerWidth()*.1)+"px)}</style>");
            offset.left = $(document).outerWidth()*.1;
        }
        else if(offset.left+title_hint.outerWidth()>$(document).outerWidth()*.9){
            offset.left = $(document).outerWidth()*.9 - title_hint.outerWidth();
            var _ = _this.offset().left+(_this.outerWidth()-title_hint.outerWidth())/2-offset.left;
            _ = "calc(50% + "+_+"px)";
            title_hint.append("<style>div.title_hint["+id+"]:after{left:"+_+"}</style>");
        }
        title_hint.css(offset).stop().css({"opacity": "1"});
    }
    var events = is_mobile?["mobile-mouseenter", "mobile-mouseleave"]:["mouseenter","mouseleave"];
    $("[title]").off(events.join(" ")).on(events[0], trigger).on(events[1], function () {
        var id = $(this).attr("data-id");
        var title_hint = $("div.title_hint["+id+"]");
        title_hint.stop().animate({"opacity": "0"}, 333, function (){
            title_hint.remove();
        });
    }).each(function () {
        $(this).attr("data-title", $(this).attr("title")).removeAttr("title");
        if(!is_mobile){
            return;
        }
        var events = ($._data(this, "events")||{});
        if(!("click" in events||["A"].indexOf(this.tagName)!==-1)){
            $(this).off("click").on("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                $("div.title_hint").remove();
                trigger.apply($(this), [e]);
                var id = $(this).attr("data-id");
                var title_hint = $("div.title_hint[" + id + "]");
                function rm() {
                    title_hint.remove();
                }
                title_hint.on("click", rm);
                setTimeout(rm, 5000);
            });
        }
    });
}
function update_scroll_hints(e){
    e.trigger("scroll");
}
function setup_scroll_hints(e, hide_start, hide_end){
    var scroll_v_hints = '<div class="scroll_v_start"></div><div class="scroll_v_end"></div>';
    var tmp = getComputedStyle(e[0]);
    var dir = 1;
    var scroll_end;
    var scroll_start;
    if (tmp["overflowY"] === "auto") {
        e.parent().append(scroll_v_hints);
        scroll_end = "div.scroll_v_end";
        scroll_start = "div.scroll_v_start";
        dir = 0;
    }
    scroll_end = e.parent().find(scroll_end);
    scroll_start = e.parent().find(scroll_start);
    if (hide_end) {
        scroll_end.remove();
    }
    if (hide_start) {
        scroll_start.remove();
    }
    e.scroll(function(_e) {
        var end;
        var start;
        if (!dir) {
            var scrollTop = _e.target.scrollTop;
            var scrollHeight = _e.target.scrollHeight;
            end = scrollTop >= scrollHeight - $(_e.target).outerHeight()-1;
            start = scrollTop === 0;
        }
        if (!hide_end) {
            if (end) {
                scroll_end.removeClass("scroll_show");
            } else {
                scroll_end.addClass("scroll_show");
            }
        }
        if (!hide_start) {
            if (start) {
                scroll_start.removeClass("scroll_show");
            } else {
                scroll_start.addClass("scroll_show");
            }
        }
    });
}
var status_msg_to;
var last_pageXY = [0,0];
if(is_mobile){
    $("div#status_msg").addClass("mobile");
    $(document).on("click", function (e) {
        if ($("div#popup_select").hasClass("show")){
            return;
        }
        if(e.pageY < 30 && ($(document).width() * 1 / 3 < e.pageX < $(document).width() * 2 / 3)){
            $("div#status_msg").addClass("show");
            function rm() {
                $("div#status_msg").removeClass("show");
            }
            setTimeout(rm, 5000);
            $("div#status_msg").on("click", rm);
        }
    });
}
else {
    $(document).on("mousemove", function (e) {
        if ($("div#popup_select").hasClass("show")){
            return;
        }
        last_pageXY = [e.pageX, e.pageY];
        var check_XY = function () {
            return last_pageXY[1] < 30 && ($(document).width() * 1 / 3 < last_pageXY[0] < $(document).width() * 2 / 3);
        }
        if (check_XY()) {
            $("div#status_msg").addClass("show");
            clearTimeout(status_msg_to);
            (function _() {
                status_msg_to = setTimeout(function () {
                    if (!check_XY()) {
                        $("div#status_msg").removeClass("show");
                    } else {
                        _();
                    }
                }, 333);
            })();
        }
    });
}
function show_status(type, msg){
    console.log(msg);
    clearTimeout(status_msg_to);
    $("div#status_msg").addClass("finish");
    setTimeout(function () {
        $("div#status_msg").removeClass("show");
        setTimeout(function () {
            $("div#status_msg div#status_icon").removeAttr("class").addClass(type);
            if(typeof msg === "string"){
                msg = "<span>"+msg+"</span>";
            }
            $("div#status_msg div.msg").html(msg);
            $("div#status_msg").removeClass("finish").addClass("show");
            status_msg_to = setTimeout(function () {
                $("div#status_msg").removeClass("show");
            }, 5000);
        }, 50);
    }, 50);
}
window.success = function(msg){
    show_status("success", msg);
}
window.failure = function(msg){
    show_status("failure", msg);
}
window.info = function(msg){
    show_status("info", msg);
}
window.warning = function(msg){
    show_status("warning", msg);
}
function update_help_hints(){
    var skip = [];
    var steps = 0;
    var seen = 0;
    function wrapper(f, cb){
        steps += 1;
        return function () {
            seen += 1;
            if(seen===steps){
                $("div#skip_help_hint").fadeOut();
            }
            f(cb);
        }
    }
    function repr(e){
        var cl = Array.from(e.classList).join(".");
        var id = e.id;
        var tn = e.tagName.toLowerCase();
        return tn+(id?"#"+id:"")+(cl?"."+cl:"");
    }
    function step1(cb){
        info("Click this top area shows last notification");
        setTimeout(function () {
            $("div#status_msg").removeClass("show");
            setTimeout(cb, 333);
        }, 3333/2);
    }
    function step2(cb){
        var l = $("div#toolbar div#tools > div[id]:visible").get();
        (function _() {
            var e = l.shift();
            if(!e||skip.length>=1){
                cb();
                return;
            }
            e = $(e);
            e.trigger((is_mobile?"mobile-":"")+"mouseenter");
            setTimeout(function () {
                e.trigger((is_mobile?"mobile-":"")+"mouseleave");
                if(skip.length>=1){
                    cb();
                    return;
                }
                setTimeout(_, 333/2);
            }, 333*2);
        })();
    }
    function step3(cb){
        var el = $("div#pages [data-title]:visible").get();
        if (el.length) {
            var els = [];
            var es = [];
            for (var i = 0; i < el.length; i++) {
                var r = repr(el[i]);
                if (els.indexOf(r) === -1) {
                    es.push(el[i]);
                    els.push(r);
                }
            }
            (function _() {
                var e = es.shift();
                if (!e||skip.length>=2) {
                    cb();
                    return;
                }
                e = $(e);
                e.trigger((is_mobile ? "mobile-" : "") + "mouseenter");
                setTimeout(function () {
                    e.trigger((is_mobile ? "mobile-" : "") + "mouseleave");
                    setTimeout(_, parseInt(e.data("interval"))||333 / 2);
                }, parseInt(e.data("duration"))||333 * 2);
            })();
        }
        else{
            cb();
        }
    }
    function stepend() {
        skip = [];
        steps = seen = 0;
    }
    $("div#skip_help_hint").off("click").on("click", function () {
        skip.push(null);
    });
    $("span.help").off("click").on("click", function () {
        if(steps!==0){
            return;
        }
        $("div#skip_help_hint").fadeIn();
        wrapper(step1, (wrapper(step2, wrapper(step3, stepend))))();
    });
}
function main () {
    var files = [];
    var all_folders = [];
    var cur_folder = window.location.hash.slice(1).split("folder=");
    var cut_file = [];
    var search_input_to;
    var traverse_cache = {};
    var get_folder_cache = {};
    var folder_name_cache = {};
    var search_in_progress = 0;
    setup_popup_select();
    function get_compilation(){
        var compilation = {
            "display_name": "",
            "drive": "",
            "root": "",
            "relative_path": "",
            "files": []
        };
        return JSON.parse(JSON.stringify(compilation));
    }
    function clear_cache() {
        all_folders = [];
        traverse_cache = {};
        get_folder_cache = {};
        folder_name_cache = {};
    }
    function get_all_folders(cb, error_cb){
        if(all_folders.length){
            return cb(all_folders);
        }
        $.post(api_endpoint, "op=get_all_folders", function (response){
            all_folders = response;
            cb(response);
        }).error(function (e) {
            typeof error_cb === "function" && error_cb(e);
        });
    }
    $("div#clone_btn").on("click", function () {
        var ta = $("div#main_page textarea#clone_link");
        var _links = ta.val();
        var key = $("div#main_page div#api_key input").val();
        if(!key){
            warning("Failed to clone<br/>Reason: No api key");
            return;
        }
        if(!_links){
            warning("Failed to clone<br/>Reason: No link(s)");
            return;
        }
        _links = _links.split("\n");
        var links = [];
        for(var i=0;i<_links.length; i++){
            if(_links[i]) {
                links.push(_links[i].split(" ")[0]);
            }
        }
        function next_link(index){
            var link = links[index];
            if(!link){
                info("Cloned "+links.length+" files");
                return;
            }
            link = link.split("/").slice(-1)[0];
            if (link) {
                $.post(api_endpoint, "op=clone_file&id="+link, function (url) {
                    console.log("$(\"div#clone_btn\").click", "link", link, "response", url);
                    url = url.split("/").slice(-1)[0];
                    $.get("https://userscloud.com/api/file/clone?key="+key+"&file_code="+url, function(response){
                        console.log("$(\"div#clone_btn\").click", "url", url, "response", response);
                        if (response["msg"] === "OK") {
                            success("Cloning &#x22EF; ("+(index+1)+"/"+links.length+")<br/>Cloned '"+link+"'");
                            links[index] = links[index] + " (Cloned to "+response["result"]["url"]+")";
                        }
                        else{
                            failure("Cloning &#x22EF; ("+(index+1)+"/"+links.length+")<br/>Failed to clone '"+link+"'");
                            links[index] = links[index] + " (Failed: "+response["msg"]+")";
                        }
                        ta.val(links.join("\n"));
                        next_link(index + 1);
                    }).error(function () {
                        console.log("$(\"div#clone_btn\").click", "url", url, "response", e.responseText);
                        failure("Cloning &#x22EF; ("+(index+1)+"/"+links.length+")<br/>Failed to clone '"+link+"'");
                        links[index] = links[index] + " (Failed: API endpoint not available)";
                        ta.val(links.join("\n"));
                        next_link(index+1);
                    });
                }).error(function (e) {
                    console.log("$(\"div#clone_btn\").click", "link", link, "response", e.responseText);
                    failure("Cloning &#x22EF; ("+(index+1)+"/"+links.length+")<br/>Failed to clone '"+link+"'");
                    links[index] = links[index] + " (Failed: Incorrect file link)";
                    ta.val(links.join("\n"));
                    next_link(index+1);
                });
            }
            else{
                next_link(index+1);
            }
        }
        next_link(0);
        info("Cloning "+links.length+" link(s)");
    });
    $("div#tools > div[id], div#main").on("click", function (){
        var _this = $(this);
        var target = $("div#pages div#"+_this.attr("id")+"_page");
        if (!target.length){
            return;
        }
        if (!notlogin) {
            window.location.hash = _this.attr("id");
        }
        function next() {
            $("div#pages").slideUp(function () {
                $("div#pages > div[id]").hide();
                target.show();
                $("div#pages").slideDown(function () {
                    update_scroll_hints($("div#pages"));
                    update_title_hints();
                    update_help_hints();
                });
            });
        }
        if(!$("div#main").hasClass("done")) {
            $("div#main").addClass("done");
            var l = $("div#toolbar").width() - $("div#main").width() - $("div#tools").outerWidth();
            if (l > $("div#tools").outerWidth(true) - $("div#tools").outerWidth()) {
                $("div#tools").addClass("done").animate({"margin-left": l}, 333, next);
            } else {
                next();
            }
        }
        else{
            next();
        }
    });
    $("div#tools div#logout").on("click", function () {
        if(!confirm("Are you sure to logout?")){
            return;
        }
        window.location = "/logout";
    });
    function loop_folder(folders, folder, result, level){
        var done = [];
        if (!level){
            level = 0;
        }
        result.push([level, folder]);
        for (var i=0; i<folders.length; i++){
            if (done.indexOf(i) !== -1){
                continue;
            }
            if (folders[i][2] === folder[0]){
                done = done.concat(loop_folder(folders, folders[i], result, level+1)[1]);
            }
        }
        return [result, done];
    }
    $("div#tools div#import").on("click", function () {
        $("div#import_page input.input").val("");
    });
    function gen_select(target) {
        get_all_folders(function (response){
            // response.sort(function (a, b) {
            //     if (!a[2]||!b[2]){
            //         return !a[2]?-1:1;
            //     }
            //     else if (a[2] === b[2]){
            //         return a[1].localeCompare(b[1]);
            //     }
            //     else{
            //         return a[2] < b[2]?-1:1;
            //     }
            // });
		    response = loop_folder(response, response[0], [])[0];
		    $(target+" select").empty();
            var options = "";
		    for(var i=0;i<response.length;i++){
                var indent = "".padStart(response[i][0], "　");//+(response[i][0]-1>=0?"":"");
		        options += "<option data-depth='"+response[i][0]+"' data-name='"+response[i][1][1]+"' value='"+response[i][1][0]+"'>"+indent+"&#x01F4C1; "+response[i][1][1]+"</option>";
            }
		    $(target+" select").html(options);
        }, function (e) {
		    $(target+" select").empty();
        });
    }
    $("div#tools div#import2").on("click", function(){
        $("div#import2_page textarea#import2_link").val("");
        gen_select("div#import2_page");
    });
    $("div#tools div#upload").on("click", function () {
        if(notlogin){
            return;
        }
        files = [];
        $("div#file_drop_zone, div#upload_btn, div#upload_target").slideDown();
        $("div#file_drop_zone").addClass("hint").empty();
        $("div#upload_progress, div#upload_results, div#upload_again, div#upload_abort_btns").slideUp();
        gen_select("div#upload_target");
    });
    if (cur_folder.length === 1){
        cur_folder = null;
    }
    else{
        cur_folder = parseInt(cur_folder.slice(-1)[0]);
    }
    function get_folder_name(id, error_cb, end_cb){
        if(id in folder_name_cache){
            end_cb(folder_name_cache[id]);
        }
        else{
            $.post(api_endpoint, "op=get_folder_name&id="+id, function (response) {
                folder_name_cache[id] = response;
                end_cb(response);
            }).error(error_cb);
        }
    }
    function get_parent_name(parent, error_cb, end_cb){
        var name = "";
        function next(response) {
            parent = response[3];
            if(!parent){
                end_cb(name);
                return;
            }
            get_folder_name(parent, error_cb, function (response) {
                name = (response||"") + "/" + name;
                get_folder(parent, error_cb, next, 1);
            });
        }
        get_folder(parent, error_cb, next, 1);
    }
    function create_compilation(data, name){
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.style = "display: none";
        var blob = new Blob([data], {type: "octet/stream"});
        var url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = name;
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    }
    $("div#files_page div#merge_folder").on("click", function () {
        var selected = $("div#files_page div#entries div.table div.td.folder").parent("div.tr.selected");
        if(!selected||!confirm("Are you sure to continue?")){
            return;
        }
        var folders = [];
        function next() {
            function next_content(index){
                var folder = folders[index];
                if(!folder){
                    return;
                }
                function _cb(e){
                    if(e){
                        success;
                    }
                    else{
                        failure;
                    }
                }
                function end_it() {
                    $("div#files_page div#entries div.table div.td.folder").parent().removeClass("selected");
                    clear_cache();
                    get_folders(cur_folder, 1);
                    next_content(index+1);
                }
                function end_cb(response){
                    var query = "op=move_file&folder="+folders[0][0];
                    if(response[1].length){
                        for(var i=0;i<response[1].length;i++) {
                            query += "&id="+response[1][i][0];
                        }
                    }
                    if(response[2].length){
                        for(var i=0;i<response[2].length;i++) {
                            query += "&id="+response[2][i][0];
                        }
                    }
                    $.post(api_endpoint, query, function (response) {
                        var query = "op=remove_folder&id="+folder[0];
                        $.post(api_endpoint, query, function (response) {
                            success;
                            end_it();
                        }).error(function (e) {
                            failure;
                            end_it();
                        });
                    }).error(function (e) {
                        failure;
                        end_it();
                    });
                }
                get_folder(folder[0], _cb, end_cb, 1);
            }
            next_content(1);
        }
        function next_folder(index) {
            var folder = selected[index];
            if(!folder){
                if(!folders.every(function (e) {
                    return e[1]===folders[0][1];
                })){
                    failure;
                    return;
                }
                next();
                return;
            }
            folder = $(folder);
            function _cb(e){
                if(e){
                    success;
                }
                else{
                    failure;
                }
            }
            function end_cb(response){
                folders.push([parseInt(folder.data("id")), response]);
                next_folder(index+1);
            }
            get_folder_name(parseInt(folder.data("id")), _cb, end_cb);
        }
        next_folder(0);
    });
    $("div#files_page div#gen_compilation").on("click", function () {
        if(!confirm("Are you sure to continue?\nThis may take a while.")){
            return;
        }
        var compilation = get_compilation();
        var failed = 0;
        var flags = [0,0,0];
        var ti = setInterval(function () {
            if(failed){
                failure("failed");
                clearInterval(ti);
                return;
            }
            if(!flags.every(function (e) {
                return !!e;
            })){
                return;
            }
            if(flags.length===3){
                return;
            }
            clearInterval(ti);
            create_compilation(JSON.stringify(compilation, 0, 4).replace(/[\u007f-\uffff]/g,
              function(c) {
                  return "\\u"+("0000"+c.charCodeAt(0).toString(16)).slice(-4);
              }
           ), compilation["relative_path"]+".json");
        }, 500);
        get_folder_name(cur_folder, function (e) {
            failed = 1;
        }, function (response) {
            compilation["relative_path"] = response;
            flags[1] = 1;
        });
        function get_parent() {
            get_parent_name(cur_folder, function (e) {
                failed = 1;
            }, function (name) {
                compilation["root"] = name;
                flags[0] = 1;
                get_files();
            });
        }
        function get_files() {
            function _cb(e) {
                failed = 1;
            }
            function loop_cb(folder, files) {
                var __i = flags.length;
                flags.push(0);
                get_parent_name(folder[1][0], _cb, function (name) {
                    for(var j=0;j<files.length;j++){
                        if(/^[a-z0-9]{40}\.zip$/.test(files[j][1])&&files[j][2]<10*1024*1024){
                            compilation["display_name"] = files[j][1].slice(0, 40);
                            continue;
                        }
                        compilation["files"].push([
                            name.replace(compilation["root"], "")+folder[1][1]+"/"+files[j][1],
                            window.location.origin+"/"+files[j][0]
                        ]);
                    }
                    flags[__i] = 1;
                });
                return function () {
                    return flags[__i];
                }
            }
            traverse_folder(cur_folder, _cb, loop_cb, function () {
                flags[2] = 1;
            }, 1);
        }
        get_parent();
    });
    $("div#files_page div#new_folder").on("click", function () {
        var name = prompt("Enter name of the new folder: ");
        if (!name){
            return;
        }
        clear_cache();
        $.post(api_endpoint, "op=new_folder&name="+name+"&parent="+cur_folder, function (response) {
            console.log("$(\"div#files_page div#new_folder\").click", "name", name, "response", response);
            success("Created new folder '"+name+"'");
            get_folders(cur_folder);
        }).error(function (e) {
            console.log("$(\"div#files_page div#new_folder\").click", "name", name, "response", e.responseText);
            failure("Failed to create new folder '"+name+"'<br/>Reason: "+e.responseText);
        });
        info("Creating new folder '"+name+"'");
    });
    $("div#files_page div#select_all").on("click", function () {
        var lis = $("div#files_page div#entries div.table div.td.file, div#files_page div#entries div.table div.td.folder:not(.parent)").parent();
        if (lis.filter(function(i, el){
            return $(el).hasClass("selected");
        }).length===lis.length){
            lis.removeClass("selected");
            info("Deselected "+lis.length+" item(s)");
        }
        else {
            lis.addClass("selected");
            info("Selected "+lis.length+" item(s)");
        }
    });
    $("div#files_page div#cut_file").on("click", function () {
        var _ = $("div#files_page div#entries div.table div.tr.selected");
        if(!_.length){
            warning("Failed to cut item(s)<br/>Reason: No item(s) selected");
            return;
        }
        cut_file = _.map(function (i, el) {
            return $(el).data("id");
        }).get();
        $(this).hide();
        $("div#file_ops div#move_file").css({"display": "flex"});
        info("Cut "+cut_file.length+" item(s)");
    });
    $("div#files_page div#move_file").on("click", function () {
        if(cut_file.indexOf(cur_folder)!==-1){
            failure("Failed to move item(s)<br/>Reason: Cannot move folder inside itself");
            return;
        }
        if(!cut_file.length||!confirm("Are you sure to continue?")){
            return;
        }
        var q = "";
        for (var i=0;i<cut_file.length; i++){
            q += "&id="+cut_file[i];
        }
        var cut_file_length = cut_file.length;
        clear_cache();
        $.post(api_endpoint, "op=move_file&folder="+cur_folder+q, function (response) {
            console.log("$(\"div#files_page div#move_file\").click", "q", q, "response", response);
            get_folders(cur_folder);
            success("Moved "+cut_file_length+" item(s)");
        }).error(function (e) {
            console.log("$(\"div#files_page div#move_file\").click", "q", q, "response", e.responseText);
            failure("Failed to move "+cut_file_length+" item(s)<br/>Reason: "+e.responseText);
        });
        info("Moving "+cut_file_length+" files");
        $("div#files_page div#cut_file").css({"display": "flex"});
        $(this).hide();
        cut_file = [];
    });
    $("div#files_page div#cancel_file").on("click", function () {
        $("div#files_page div#entries div.table div.tr").removeClass("selected");
        $("div#files_page div#cut_file").css({"display": "flex"});
        $("div#file_ops div#move_file").hide();
        cut_file = [];
        info("Cancelled");
    });
    function folder_access(e, cb) {
        e.preventDefault();
        e.stopPropagation();
        var access = $(this).data("title");
        var folder = $(this).closest("div.tr").data("id");
        $.post(api_endpoint, "op=folder_access&id="+folder, function(){
            get_folders(cur_folder);
            success(access+"d folder '"+folder+"'");
            typeof cb === "function" && cb();
        }).error(function (e) {
            failure("Failed to "+access.toLowerCase()+" folder '"+folder+"'<br/>Reason: "+e.responseText);
            typeof cb === "function" && cb();
        });
    }
    $("div#files_page div#share_folders").on("click", function (e) {
        var folders = $("div#files_page div#entries div.table div.tr.selected span.folder_access");
        if(!folders.length){
            warning("Failed to rename folder(s)<br/>Reason: No folder(s) selected");
            return;
        }
        if(!confirm("Are you sure to share the folder(s)?")){
            return;
        }
        function next_folder(index) {
            var folder = folders[index];
            if(!folder){
                return;
            }
            folder_access.apply($(folder), [e, function () {
                next_folder(index+1);
            }]);
        }
        next_folder(0);
    });
    $("div#files_page div#rename_folder").on("click", function () {
        var folders = $("div#files_page div#entries div.table div.td.folder:not(.parent)").parent("div.tr.selected");
        if(!folders.length){
            warning("Failed to rename folder(s)<br/>Reason: No folder(s) selected");
            return;
        }
        function next_folder(index){
            clear_cache();
            var folder = folders[index];
            if(!folder){
                get_folders(cur_folder);
                info("Renamed "+folders.length+" folder(s)");
                return;
            }
            var name = prompt("Enter new name:");
            if(!name){
                next_folder(index+1);
                return;
            }
            $.post(api_endpoint, "op=rename_folder&id="+$(folder).data("id")+"&name="+encodeURIComponent(name), function (response) {
                console.log("$(\"div#files_page div#rename_folder\").click", "name", name, "response", response);
                success("Renamed folder '"+name+"'");
                next_folder(index+1);
            }).error(function (e) {
                console.log("$(\"div#files_page div#rename_folder\").click", "name", name, "response", e.responseText);
                failure("Failed to rename folder '"+name+"'<br/>Reason: "+e.responseText);
            });
        }
        info("Renaming "+folders.length+" folder(s)");
        next_folder(0);
    });
    function traverse_folder(folder_id, error_cb, loop_cb, end_cb, use_cache) {
        get_all_folders(function (response) {
            // response.sort(function (a, b) {
            //     if (!a[2] || !b[2]) {
            //         return !a[2] ? -1 : 1;
            //     } else if (a[2] === b[2]) {
            //         return a[1].localeCompare(b[1]);
            //     } else {
            //         return a[2] < b[2] ? -1 : 1;
            //     }
            // });
            var folders = loop_folder(response, response.filter(function(a){
                return a[0] === folder_id;
            })[0], [])[0];
            function next_folder(index){
                var folder = folders[index];
                if (!folder){
                    typeof end_cb === "function" && end_cb();
                    return;
                }
                function cb(response){
                    var loop_cb_r = typeof loop_cb === "function" && loop_cb(folder, response[2]);
                    if(loop_cb_r===false){
                        return;
                    }
                    if (typeof loop_cb_r === "function"){
                        var loop_cb_r_ti = setInterval(function () {
                            if(!loop_cb_r()){
                                return;
                            }
                            clearInterval(loop_cb_r_ti);
                            next_folder(index+1);
                        }, 10);
                        return;
                    }
                    next_folder(index+1);
                }
                get_folder(folder[1][0], function (e) {
                    next_folder(index+1);
                }, cb, use_cache);
            }
            next_folder(0);
        }, function(e){
            error_cb(0);
        });
    }
    $("div#popup_item_property").on("click", function () {
        $("div#item_property span[id]").empty();
        $(this).removeClass("show");
    }).find("div#item_property_content").on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
    });
    $("div#files_page div#properties").on("click", function () {
        if(!confirm("Are you sure to continue?\nThis may take a while.")){
            return;
        }
        var selected = $("div#files_page div#entries div.table div.tr.selected");
        if(!selected.length){
            var selected_folders = $("<div data-id='"+cur_folder+"'/>");
            var selected_files = [];
        }
        else {
            var selected_folders = selected.find("div.td.folder").parent();
            var selected_files = selected.find("div.td.file").parent();
        }
        var stats = {
            "location": null,
            "folders": [],
            "files": [],
            "stats": {},
            "total_size": 0
        };
        var flags = [0,0,0];
        var cancel_flag = 0;
        var targets = [];
        var orphans = [];
        var popup_item_property = $("div#popup_item_property");
        function gen_result() {
            function next(length, result) {
                var content = gen_search_result(result, targets, orphans);
                if(!content){
                    return;
                }
                setup_search_result(popup_item_property.find("div#item_property h3 span#item_tree_view").html(content));
            }
            search_in_cache(".", targets, next);
        }
        function gen_property(done){
            var items_repr = "";
            items_repr += stats["folders"].length+" folder(s)";
            if(stats["files"].length){
                if(items_repr){
                    items_repr += done?" and ":", ";
                }
                items_repr += stats["files"].length+" file(s)";
            }
            if(!done) {
                items_repr += " and counting";
            }
            var item_exts = {};
            for(var i=0;i<stats["files"].length;i++){
                var ext = stats["files"][i][1].split(".");
                if(ext.length>=2){
                    ext = "."+ext.slice(-1)[0].toLowerCase();
                    if(!(ext in item_exts)){
                        item_exts[ext] = 0;
                    }
                    item_exts[ext] += 1;
                }
            }
            var item_exts_keys = Object.keys(item_exts).sort(function(a,b){return item_exts[b]-item_exts[a]});
            var item_types = "<table>";
            for(var i=0;i<item_exts_keys.length;i++){
                var k = item_exts_keys[i];
                item_types += "<tr>";
                item_types += "<td>"+k+"</td>";
                item_types += "<td>"+item_exts[k]+"</td>";
                item_types += "</tr>";
            }
            item_types += "</table>";
            popup_item_property.find("div#item_property_title h2 span.quote").html(items_repr);
            popup_item_property.find("div#item_property h3 span#item_location").html(stats["location"]);
            popup_item_property.find("div#item_property h3 span#item_size").html(format_size(stats["total_size"], 0)+" ("+stats["total_size"]+" iB)");
            popup_item_property.find("div#item_property h3 span#item_types").html(item_types);
            var item_stats = stats["stats"];
            var item_stats_keys = Object.keys(item_stats).sort(function(a,b){return item_stats[b][0]-item_stats[a][0]});
            var item_distribution = "";
            for(var i=0;i<item_stats_keys.length;i++){
                var k = item_stats_keys[i];
                item_distribution += "<tr>";
                item_distribution += "<td>"+(k||stats["location"])+"</td>";
                item_distribution += "<td>"+(item_stats[k][0]/stats["total_size"]*100).toFixed(2)+"%</td>";
                item_distribution += "<td>"+format_size(item_stats[k][0], 0)+"<br/>"+item_stats[k][0]+" iB</td>";
                item_distribution += "<td>"+
                    (!item_stats[k][1]?"":item_stats[k][1]+" folder(s)")+
                    (!item_stats[k][2]?"":(item_stats[k][1]?"<br/>":"")+item_stats[k][2]+" file(s)")+
                    "</td>";
                item_distribution += "</tr>";
            }
            item_distribution = "<table>" + item_distribution + "</table>";
            popup_item_property.find("div#item_property h3 span#item_distribution").html(item_distribution);
            popup_item_property.addClass("show");
            done&&gen_result();
        }
        var ti = setInterval(function () {
            if(!flags.every(function (e) {
                return !!e;
            })){
                return;
            }
            clearInterval(ti);
            gen_property(1);
        }, 500);
        get_parent_name(cur_folder, function (e) {
            flags[2] = 1;
        }, function (response) {
            get_folder_name(cur_folder, function (e) {
                    flags[2] = 1;
                }, function (name) {
                    stats["location"] = response+name;
                    flags[2] = 1;
                });
        });
        if(selected_files.length){
            function next(response) {
                var files_size = 0;
                var file_count = 0;
                var files_id = selected_files.map(function(i, e){
                    return $(e).data("id");
                }).get();
                for(var j=0; j<response[2].length;j++){
                    var file = response[2][j];
                    if(files_id.indexOf(file[0])===-1){
                        continue;
                    }
                    orphans.push(file);
                    stats["total_size"] += file[2];
                    files_size += file[2];
                    file_count += 1;
                }
                stats["files"] = stats["files"].concat(orphans);
                stats["stats"]["Orphan Item(s)"] = [files_size, 0, file_count];
                flags[0] = 1;
                gen_property();
            }
            get_folder(cur_folder, function (e) {
                flags[0] = 1;
            }, next, 1);
        }
        else{
            flags[0] = 1;
        }
        function next_folder(index) {
            if(cancel_flag){
                return;
            }
            function _cb(r){
                if(r){
                    success;
                }
                else{
                    failure;
                }
                next_folder(index+1);
            }
            var folder_size = 0;
            var folder_count = 0;
            var file_count = 0;
            function end_cb(){
                if(cancel_flag){
                    return;
                }
                stats["stats"][folder.find("div.td.folder").html()||""] = [folder_size, folder_count, file_count];
                _cb(1);
            }
            function loop_cb(folder, files){
                if(cancel_flag){
                    return false;
                }
                targets.push(folder);
                folder_count += 1;
                stats["folders"].push(folder);
                var folder_id = folder[1][0];
                for(var j=0; j<files.length;j++){
                    var file = files[j];
                    stats["files"].push(file);
                    stats["total_size"] += file[2];
                    folder_size += file[2];
                }
                file_count += files.length;
                traverse_cache[folder_id] = [folder[1], files];
                gen_property();
            }
            var folder = selected_folders[index];
            if(!folder){
                flags[1] = 1;
                return;
            }
            folder = $(folder);
            traverse_folder(parseInt(folder.data("id")), _cb, loop_cb, end_cb, 1);
        }
        function cancel_handler() {
            cancel_flag = 1;
            clearInterval(ti);
            $(this).off("click", cancel_handler);
        }
        popup_item_property.on("click", cancel_handler);
        next_folder(0);
        info("Collecting properties &#x22EF;<br/>Please wait");
    });
    $("div#files_page div#remove_file").on("click", function () {
        var selected = $("div#files_page div#entries div.table div.tr.selected");
        if (!selected.length){
            warning("Failed to remove item(s)<br/>Reason: No item(s) selected");
            return;
        }
        if(!confirm("Are you sure to continue?\nRemove may take a while.")){
            return;
        }
        var selected_files = selected.find("div.td.file").parent();
        var selected_folders = selected.find("div.td.folder").parent();
        var q = "";
        for (var i=0;i<selected_files.length; i++){
            q += "&id="+selected_files.eq(i).data("id");
        }
        if (q) {
            $.post(api_endpoint, "op=remove_file" + q, function (response) {
                console.log("$(\"div#files_page div#remove_file\").click", "q", q, "response", response);
                success("Removed "+selected_files.length+" file(s)");
                get_folders(cur_folder);
            }).error(function (e) {
                console.log("$(\"div#files_page div#remove_file\").click", "q", q, "response", e.responseText);
                failure("Failed to remove "+selected_files.length+" file(s)<br/>Reason: "+e.responseText);
            });
        }
        function next_folder(index){
            var files = [];
            var folders = [];
            clear_cache();
            function _cb(r){
                if(r){
                    success("Removing folder(s) &#x22EF; ("+(index+1)+"/"+selected_folders.length+")<br/>Removed folder '"+folder.data("id")+"'");
                }
                else{
                    failure("Removing folder(s) &#x22EF; ("+(index+1)+"/"+selected_folders.length+")<br/>Failed to remove folder '"+folder.data("id")+"'");
                }
                next_folder(index+1);
            }
            function loop_cb(folder, _files){
                folders.push(folder);
                for(var j=0;j<_files.length;j++){
                    files.push(_files[j][0]);
                }
            }
            function end_cb() {
                function next(){
                    var q = "";
                    for (var i = 0; i < folders.length; i++) {
                        if (q) {
                            q += "&";
                        }
                        q += "id=" + folders[i][1][0];
                    }
                    $.post(api_endpoint, "op=remove_folder&"+q, function () {
                        _cb(1);
                    }).error(function (e) {
                        _cb(0);
                    });
                }
                if (files.length) {
                    var q = "";
                    for (var i = 0; i < files.length; i++) {
                        if (q) {
                            q += "&";
                        }
                        q += "id=" + files[i];
                    }
                    $.post(api_endpoint, "op=remove_file&" + q, function () {
                        next();
                    }).error(function (e) {
                        next();
                    });
                }
                else{
                    next();
                }
            }
            var folder = selected_folders[index];
            if(!folder){
                info("Removed "+selected_folders.length+" folder(s)");
                get_folders(cur_folder);
                return;
            }
            folder = $(folder);
            traverse_folder(parseInt(folder.data("id")), _cb, loop_cb, end_cb);
        }
        info("Removing "+selected_files.length+" files(s)<br/>Removing "+selected_folders.length+" folder(s)");
        next_folder(0);
    });
    $("div#files_page div#search_item").on("click", function () {
        var input = $("div#files_page div#search_input input.input").val("").parent();
        input[input.is(":visible")?"slideUp":"show"]();
    });
    var click_close_handler = function () {
        $("div#search_result").empty();
        $(this).removeClass("show");
    };
    function setup_search_result(result_parent, file_op) {
        result_parent.find("div.folder span").on("click", function () {
            $(this).toggleClass("collapsed").parent().nextAll().slideToggle();
        });
        if(!file_op){
            return;
        }
        result_parent.find("div.file").on("click", function () {
            $(this).toggleClass("selected");
        });
        result_parent.find("div.file a").on("click", function (e) {
            e.stopPropagation();
        });
        var file_ops = $("div#files_page div#file_ops").clone();
        file_ops.children().not("div#cut_file, div#cancel_file, div#select_all, div#remove_file").remove();
        result_parent.prev("div#file_ops").remove();
        result_parent.before(file_ops);
        file_ops.find("div#cut_file").on("click", function () {
            cut_file = result_parent.find("div.file.selected").map(function (i, e) {
                return $(e).data("id");
            }).get();
            info;
        });
        file_ops.find("div#cancel_file").on("click", function () {
            cut_file = [];
            result_parent.find("div.file").removeClass("selected");
            info;
        });
        file_ops.find("div#select_all").on("click", function () {
            var files = result_parent.find("div.file");
            if(files.length === files.filter(function(i, el){
                return $(el).hasClass("selected");
            }).length){
                files.removeClass("selected");
            }
            else{
                files.addClass("selected");
            }
            info;
        });
        file_ops.find("div#remove_file").on("click", function () {
            var files = result_parent.find("div.file.selected");
            if(!files.length||!confirm("Are you sure to continue?")){
                return;
            }
            $.post(api_endpoint, "op=remove_file&"+files.map(function (i, e) {
                return "id="+$(e).data("id");
            }).get().join("&"), function(response){
                success;
            }).error(function (e) {
                failure;
            });
            info;
        });
    }
    function gen_search_result(result, targets, orphans) {
        var tmp = 0;
        for(var i=0;i<result.length;i++){
            if(!result[i][1].length){
                tmp += 1;
            }
        }
        if(tmp === result.length){
            return;
        }
        var prev_folder = result[0][0][0];
        var prev_depth = -1;
        var content = "";
        for(var i=0;i<result.length;i++){
            var depth = 0;
            for(var j=0; j<targets.length;j++){
                if(targets[j][1][0]===result[i][0][0]){
                    depth = targets[j][0];
                    break;
                }
            }
            var b=[
                depth < prev_depth,
                depth > prev_depth,
                depth===prev_depth&&prev_folder!==result[i][0][0]
            ];
            if (b[0]||b[2]){
                for(var _depth=prev_depth; _depth>(b[0]?depth:prev_depth)-1; _depth--){
                    content += "</div>";
                    // console.log("".padStart(_depth*4, " ")+"</div>");
                }
            }
            if(b.some(function (e) {
                return e;
            })){
                // console.log("".padStart((depth)*4, " ")+"<div class='depth"+depth+"'>");
                content += "<div class='depth"+(depth?1:0)+"'"+(depth&&orphans?" style='display:none'":"")+">";
                content += "<div class='folder'>" +
                    "<span class='icon"+(orphans?" collapsed":"")+"'>&#x01F4C1;</span>" +
                    " <a href='/#folder="+result[i][0][0]+"' target='_blank'>"+result[i][0][1]+"</a>" +
                    "</div>";
            }
            if(result[i][1].length){
                // console.log("".padStart((depth+1)*4, " ")+"file")
                content += "<div class='file depth1'"+(orphans?" style='display:none'":"")+" data-id='"+result[i][1][0]+"'>" +
                    "<span class='icon'>&#x01F4C4;</span>" +
                    " <a href='/"+result[i][1][0]+"' target='_blank'>"+result[i][1][1]+"</a>" +
                    " <span class='size'>"+format_size(result[i][1][2], 0)+"</span>" +
                    "</div>";
            }
            prev_depth = depth;
            prev_folder = result[i][0][0];
        }
        var depth = 0;
        for(var _depth=prev_depth; _depth>depth-1; _depth--){
            content += "</div>";
            // console.log("".padStart((_depth)*4, " ")+"</div>");
        }
        for(var i=0;i<(orphans||[]).length;i++){
            content += "<div class='file depth0'><span>&#x01F4C4;</span> <a href='/"+orphans[i][0]+"' target='_blank'>"+orphans[i][1]+"</a></div>";
        }
        // console.log(content)
        return content;
    }
    function search_in_cache(regex, targets, cb){
        var result = [];
        var targets2 = JSON.parse(JSON.stringify(targets));
        for(var i=0; i<targets2.length;i++){
            targets2[i] = targets2[i][1][0];
        }
        var parents = [];
        function push_parents(folder) {
            for(var i=0;i<targets.length;i++){
                if(folder === targets[i][1][0]){
                    var parent = targets[i][1][2];
                    if(parent !== null && parents.indexOf(parent)===-1){
                        parents.push(parent);
                        push_parents(parent);
                    }
                }
            }
        }
        var matches = 0;
        for(var folder in traverse_cache){
            var _folder = traverse_cache[folder][0];
            if(targets2.indexOf(_folder[0])===-1){
                continue;
            }
            var files = traverse_cache[folder][1];
            var found = 0;
            for(var i=0;i<files.length;i++){
                if (regex instanceof RegExp){
                    if(regex.test(files[i][1])){
                        result.push([_folder, files[i]]);
                        matches += 1;
                        found = 1;
                    }
                }
                else{
                    if(files[i][1].indexOf(regex)!==-1){
                        result.push([_folder, files[i]]);
                        matches += 1;
                        found = 1;
                    }
                }
            }
            if(found){
                parents.push(_folder[0]);
                push_parents(_folder[0]);
            }
            else{
                found = 0;
                for(var i=0;i<targets.length;i++){
                    if(_folder[0] === targets[i][1][2]){
                        found = 1;
                    }
                }
                if(found){
                    result.push([_folder, []]);
                }
            }
        }
        get_all_folders(function (response){
            response = loop_folder(response, response[0], [])[0];
            function get_index(c) {
                for(var i=0;i<response.length;i++){
                    if(response[i][1][0]===c){
                        return i;
                    }
                }
                return -1;
            }
            cb(matches, result.filter(function (a){
                return parents.indexOf(a[0][0]) !== -1;
            }).sort(function (a, b) {
                var diff = get_index(a[0][0])-get_index(b[0][0]);
                if(diff){
                    return diff;
                }
                diff = a[1][1].localeCompare(b[1][1]);
                return diff;
            }));
        });
    }
    $("div#files_page div#search_input input.input").on("keyup", function () {
        if(search_in_progress){
            info("too busy");
            return;
        }
        var _this = $(this);
        var cancel_flag = 0;
        var to;
        function start_search() {
            _this.trigger("blur");
            if(!_this.val()){
                return;
            }
            search_in_progress = 1;
            var regex = _this.val();
            try{
                regex = new RegExp().compile(regex);
            }
            catch (e){
                ;
            }
            var targets = [];
            function _cb(r) {
                if(r){
                    success;
                }
                else{
                    failure;
                }
            }
            function loop_cb(folder, files) {
                if(cancel_flag){
                    return false;
                }
                targets.push(folder);
                traverse_cache[folder[1][0]] = [folder[1], files];
            }
            var prev_result_length = -1;
            function gen_result(done) {
                function next(length, result) {
                    if(length===prev_result_length){
                        return;
                    }
                    interval = length*4;
                    if(interval<min_interval){
                        interval = min_interval;
                    }
                    prev_result_length = length;
                    var content = gen_search_result(result, targets);
                    if(done&&!content){
                        info("no result");
                        return;
                    }
                    var popup_search_result = $("div#popup_search_result").addClass("show").off("click", click_close_handler).on("click", click_close_handler);
                    popup_search_result.find("div#search_result_content").off("click").on("click", function (e) {
                        e.stopPropagation();
                    });
                    popup_search_result.find("div#search_result_title h2 span.quote").html(_this.val());
                    popup_search_result.find("div#search_result_title h2 span.count").html(length+(done?"":" and counting"));
                    setup_search_result(popup_search_result.find("div#search_result").html(content), 1);
                }
                search_in_cache(regex, targets, next);
            }
            var min_interval = 1000;
            var interval = min_interval;
            function timeout(){
                to = setTimeout(function () {
                    gen_result();
                    timeout();
                }, interval);
            }
            timeout();
            function end_cb() {
                search_in_progress = 0;
                if(cancel_flag){
                    return;
                }
                clearTimeout(to);
                _cb(1);
                gen_result(1);
            }
            traverse_folder(cur_folder, _cb, loop_cb, end_cb, 1);
        }
        clearTimeout(search_input_to);
        search_input_to = setTimeout(function () {
            info("searching");
            start_search();
            function cancel_handler(){
                cancel_flag = 1;
                search_in_progress = 0;
                clearTimeout(to);
                $(this).off("click", cancel_handler);
            }
            $("div#popup_search_result").on("click", cancel_handler);
        }, 1000);
    });
    $("div#files_page div#goto_import").on("click", function () {
        $("div#tools div#import").trigger("click");
    });
    $("div#files_page div#goto_import2").on("click", function () {
        $("div#tools div#import2").trigger("click");
    });
    $("div#import_target input").on("keyup change", function () {
        var fld_id = $(this).val();
        if(!fld_id){
            return;
        }
        fld_id = fld_id.match(/(fld_id=)?([0-9]+)$/)[2];
        if(!fld_id){
            return;
        }
        $(this).val(fld_id);
    });
    $("div#import2_page div#import2_btn").on("click", function () {
        var ta = $("div#import2_page textarea#import2_link");
        var target = $("div#import2_target select").val();
        var _links = ta.val();
        if(!_links){
            warning("Failed to import<br/>Reason: No link(s)");
            return;
        }
        if(!target){
            warning("Failed to import link(s)<br/>Reason: No import destination");
            return;
        }
        if(!confirm("Are you sure to continue?\nImport may take a while.")){
            return;
        }
        _links = _links.split("\n");
        var links = [];
        for(var i=0;i<_links.length; i++){
            if(_links[i]) {
                links.push(_links[i].split(" ")[0]);
            }
        }
        function next_link(index){
            var link = links[index];
            if(!link){
                info("Imported "+links.length+" files");
                clear_cache();
                return;
            }
            link = link.split("/").slice(-1)[0];
            if (link) {
                $.post(api_endpoint, "op=import2&"+(link[0]==="#"?"dir="+link.slice(8):"id="+link)+"&folder="+target, function (response) {
                    console.log("$(\"div#import2_page div#import2_btn\").click", "link", link, "response", response);
                    success("Importing &#x22EF; ("+(index+1)+"/"+links.length+")<br/>Imported '"+link+"'");
                    links[index] = links[index] + " (Imported)";
                    ta.val(links.join("\n"));
                    next_link(index+1);
                }).error(function (e) {
                    console.log("$(\"div#import2_page div#import2_btn\").click", "link", link, "response", e.responseText);
                    failure("Importing &#x22EF; ("+(index+1)+"/"+links.length+")<br/>Failed to import '"+link+"'");
                    links[index] = links[index] + "  (Failed: "+e.responseText+")";
                    ta.val(links.join("\n"));
                    next_link(index+1);
                });
            }
            else{
                next_link(index+1);
            }
        }
        next_link(0);
        info("Importing "+links.length+" link(s)");
    });
    function convert_utf8(s){
        var max=5;
        var i=0;
        while(1){
            try{
                if(i>max){
                    throw new Error();
                }
                s = decodeURIComponent(s.split("").map(function(e){
                    return "%"+e.charCodeAt(0).toString(16);
                }).join(""));
                s = $("<p/>").html(s).text();
                i++;
            }
            catch(e){
                return s;
            }
        }
    }
    $("div#import_page div#import_btn").on("click", function () {
        var api_key = $("div#import_page div#api_key input").val();
        if(!api_key){
            warning("Failed to import<br/>Reason: No api key");
            return;
        }
        var fld_id = $("div#import_target input").val();
        if(fld_id){
            fld_id = fld_id.match(/(fld_id=)?([0-9]+)$/)[2];
            if(!fld_id){
                warning("Failed to import<br/>Reason: No api key");
                return;
            }
        }
        else{
            fld_id = "0";
        }
        if(!confirm("Are you sure to continue?\nImport may take a while.")){
            return;
        }
        var queue = [[fld_id, (fld_id==="0"?"/":"/imported_folder_"+fld_id+"/")]];
        var traverse = 0;
        var result = [];
        var file_done = 0;
        function next_folder() {
            if(!queue.length){
                traverse = 1;
                return;
            }
            var [fld_id, path] = queue.shift();
            $.get("https://userscloud.com/api/folder/list?key="+api_key+"&fld_id="+fld_id, function (response) {
                console.log("$(\"div#import_page div#import_btn\").click", "fld_id", fld_id, "response", response);
                if (response["msg"] === "OK") {
                    var files = response["result"]["files"];
                    var folders = response["result"]["folders"];
                    for (var i = 0; i < files.length; i++) {
                        result.push([path, files[i]["file_code"], convert_utf8(files[i]["name"])]);
                    }
                    for (var i = 0; i < folders.length; i++) {
                        queue.push([folders[i]["fld_id"], path + convert_utf8(folders[i]["name"]) + "/"]);
                    }
                    next_folder();
                }
                else{
                    warning("Importing &#x22EF; ("+file_done+"/"+(file_done+result.length)+")<br/>Failed to traverse folder '"+fld_id+"'");
                    next_folder();
                }
            }).error(function (e) {
                console.log("$(\"div#import_page div#import_btn\").click", "fld_id", fld_id, "response", e.responseText);
                warning("Importing &#x22EF; ("+file_done+"/"+(file_done+result.length)+")<br/>Failed to traverse folder '"+fld_id+"'");
                next_folder();
            });
        }
        var dummy_key;
        function next_file(){
            var file = result.shift();
            if(!file){
                if(!traverse){
                    setTimeout(next_file, 500);
                }
                else{
                    clear_cache();
                    info("Imported "+file_done+" files");
                }
                return;
            }
            $.get("https://userscloud.com/api/file/clone?key="+dummy_key+"&file_code="+file[1], function (response) {
                console.log("$(\"div#import_page div#import_btn\").click", "file[1]", file[1], "response", response);
                if (response["msg"] === "OK") {
                    var query = [
                        ["op", "import_file"],
                        ["code", response["result"]["filecode"]],
                        ["path", file[0]],
                        ["name", file[2]],
                    ]
                    for(var i=0;i<query.length;i++){
                        query[i][1] = encodeURIComponent(query[i][1]);
                        query[i] = query[i].join("=");
                    }
                    $.post(api_endpoint, query.join("&"), function () {
                        console.log("$(\"div#import_page div#import_btn\").click", "query.join(\"&\")", query.join("&"));
                        file_done += 1;
                        success("Importing &#x22EF; ("+file_done+"/"+(file_done+result.length)+")<br/>Imported '"+file[2]+"'");
                        next_file();
                    }).error(function (e) {
                        console.log("$(\"div#import_page div#import_btn\").click", "response", e.responseText);
                        file_done += 1;
                        failure("Importing &#x22EF; ("+file_done+"/"+(file_done+result.length)+")<br/>Failed to import '"+file[2]+"'");
                        next_file();
                    });
                }
                else{
                    file_done += 1;
                    warning("Importing &#x22EF; ("+file_done+"/"+(file_done+result.length)+")<br/>Failed to clone '"+file[2]+"'");
                    next_file();
                }
            }).error(function (e) {
                console.log("$(\"div#import_page div#import_btn\").click", "file[1]", file[1], "response", e.responseText);
                file_done += 1;
                warning("Importing &#x22EF; ("+file_done+"/"+(file_done+result.length)+")<br/>Failed to clone '"+file[2]+"'");
                next_file();
            });
        }
        $.post(api_endpoint, "op=get_dummy_api", function (response) {
            console.log("$(\"div#import_page div#import_btn\").click", "response", response);
            dummy_key = response;
            next_folder();
            next_file();
        }).error(function (e) {
            console.log("$(\"div#import_page div#import_btn\").click", "response", e.responseText);
            failure("Failed to import<br/>Reason: No dummy api key");
        });
        info("Importing &#x22EF;<br/>Please wait");
    });
    function get_folder(folder, error_cb, end_cb, use_cache){
        if(use_cache&&folder&&folder in get_folder_cache){
            end_cb(get_folder_cache[folder]);
        }
        else{
            $.post(api_endpoint, "op=get_folders"+(folder?"&id="+folder:""), function (response) {
                get_folder_cache[folder] = response;
                end_cb(response);
            }).error(error_cb);
        }
    }
    function get_folders(folder, use_cache) {
        get_folder(folder, function (e) {
            $("div#files_page div#entries").empty().html("<p>Failed to get folder!<br/>Refresh might help!</p>");
            failure("Failed to get folder '"+folder+"'<br/>Reason: "+e.responseText);
        }, function (response){
            var [_cur_folder, folders, files, parent_folder] = response;
            cur_folder = parseInt(_cur_folder);
            if(notlogin&&!parent_folder){
                get_folder_name(cur_folder, function (e) {
                    failure;
                }, function (response) {
                    response = response||"Home";
                    var h2 = $("div#entries").prevAll("h2");
                    var h2d = h2.find("div.cwd");
                    if(!h2d.length) {
                        h2.get(0).childNodes[1].data = "";
                    }
                    else{
                        h2d.remove();
                    }
                    var h2c = h2.children();
                    h2c.eq(0).after("<div class='cwd' title='"+response+"'>"+response+"</div>");
                });
            }
            if (!folder) {
                window.location.hash = "folder=" + cur_folder;
                return;
            }
            var list = "<ul"+(notlogin?" class='notlogin'":"")+">";
            var table = "<div class='table"+(notlogin?" notlogin":"")+"'>";
            folders.sort(function(a, b){
                return a[1].localeCompare(b[1]);
            });
            files.sort(function(a, b){
                return a[1].localeCompare(b[1]);
            });
            if (parent_folder){
                var link = "<a class='folder parent' href='#folder="+parent_folder+"' title='Back'>&#x2935;&#xFE0F;</a>";
                table += "<div class='tr' data-id='"+parent_folder+"'>";
                table += "<div class='td'>&#x01F4C1;</div>";
                table += "<div class='td folder parent' colspan>‥</div>";
                if(!notlogin) {
                    table += "<div class='td'>"+link+"</div>";
                }
                table += "</div>";
            }
            for (var i=0; i<folders.length; i++){
                var link = "<a class='folder' href='#folder="+folders[i][0]+"' title='Browse'>&#x2935;&#xFE0F;</a>";
                var copy = "<a class='copy_name' href='#folder="+folders[i][0]+"' title='Copy Name<br/><i>"+folders[i][1]+"</i>'>&#x01F4CB;</a>";
                table += "<div class='tr' data-id='"+folders[i][0]+"'>";
                table += "<div class='td'><span class='folder_access"+(folders[i][2]||notlogin?" public":"")+"'"+(
                    notlogin?"":" title='"+(folders[i][2]?"Revoke":"Share")+"'"
                )+"><span>&#x01F4C1;</span></span></div>";
                table += "<div class='td folder' colspan>"+folders[i][1]+"</div>";
                table += "<div class='td'>"+copy+"</div>";
                if(!notlogin) {
                    table += "<div class='td'>"+link+"</div>";
                }
                table += "</div>";
            }
            var has_compilation = 0;
            for (var i=0; i<files.length; i++){
                var is_compilation = /^[a-z0-9]+\.zip$/.test(files[i][1])&&files[i][2]<10*1024*1024;
                if (is_compilation){
                    has_compilation = 1;
                }
                var a = [
                    "<a"+(notlogin?"":" class='file'")+" href='/"+files[i][0]+"'"+(notlogin?"":" title='Visit'")+" target='_blank'>",
                    "</a>"
                ];
                var copy = "<a class='copy_name' href='#' title='Copy Name<br/><i>"+files[i][1]+"</i>'>&#x01F4CB;</a>";
                var link = a[0]+"&#x2935;&#xFE0F;"+a[1];
                table += "<div class='tr' data-id='"+files[i][0]+"'>";
                table += "<div class='td'>"+(is_compilation?"&#x01F4BC;":"&#x01F4C4;")+"</div>";
                table += "<div class='td file' colspan>"+(notlogin?a[0]:"")+files[i][1]+(notlogin?a[1]:"")+"</div>";
                table += "<div class='td size'>"+format_size(files[i][2], 0)+"</div>";
                table += "<div class='td'>"+copy+"</div>";
                if(!notlogin) {
                    table += "<div class='td'>"+link+"</div>";
                }
                table += "</div>";
            }
            if(!folders.length&&!files.length){
                table += "<div class='tr'><div class='td empty' colspan>Empty Folder"+(parent_folder?"":"<br/>Try Import Buttons Below")+"</div></div>";
            }
            table += "</table>";
            $("div#files_page div#entries").empty().html(table);
            $("div#files_page div#entries div.table a.copy_name").on("click", function(e){
                e.preventDefault();
                e.stopPropagation();
                var title = $(this).parent().prevAll("div.file, div.folder").html();
                var temp = $("<input>");
                $("body").append(temp);
                temp.val(title).trigger("select");
                document.execCommand("copy");
                temp.remove();
            });
            $("div#files_page div#how_to_download").hide();
            $("div#files_page div#search_input").hide();
            if(notlogin){
                $("div#files_page div#entries div.table div.td.folder").parent().on("click", function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    get_folders($(this).data("id"), 1);
                });
                if(has_compilation){
                    $("div#files_page div#how_to_download").show();
                }
            }
            else{
                $("div#files_page div#entries div.table a.file, div#files_page div#entries div.table a.folder").on("click", function (e) {
                    e.stopPropagation();
                });
                $("div#files_page div#entries div.table span.folder_access").on("click", function (e) {
                    var access = $(this).data("title");
                    if(!confirm("Are you sure to "+access.toLowerCase()+" the folder?")){
                        return;
                    }
                    folder_access.apply($(this), [e, null]);
                });
                $("div#files_page div#entries div.table div.td.file, div#files_page div#entries div.table div.td.folder:not(.parent)").parent().on("click", function (e) {
                    $(this).toggleClass("selected");
                    if ( document.selection ) {
                        document.selection.empty();
                    }
                    else if ( window.getSelection ) {
                        window.getSelection().removeAllRanges();
                    }
                }).each(function(){
                    if(cut_file.indexOf($(this).data("id"))!==-1){
                        $(this).addClass("selected");
                    }
                });
            }
            update_scroll_hints($("div#pages"));
            update_title_hints();
            update_help_hints();
        }, use_cache);
    }
    $("div#tools div#files").on("click", function () {
        if(notlogin){
            return;
        }
        cut_file = [];
        $("div#cut_file").show();
        $("div#move_file").hide();
        get_folders(null, 1);
    });
    $("div#login_page input.input").on("keydown", function (e) {
        if(e.key === "Enter") {
            $("div#login_btn").trigger("click");
        }
    });
    $("div#login_btn").on("click", function () {
        $.post(api_endpoint, "op=login&username="+$("div#username input").val()+"&password="+$("div#password input").val(), function(response){
            console.log("$(\"div#login_btn\").click", "response", response);
            window.location.reload();
        }).error(function (e) {
            failure("Failed to login<br/>Reason: "+e.responseText);
        });
    });
    function format_size(size, pad) {
        var i = size === 0 ? 0 : Math.floor( Math.log(size) / Math.log(1024) );
        size = ((size/Math.pow(1024, i)).toFixed(2)*1)+" "+["iB", "KiB", "MiB", "GiB", "TiB"][i];
        if (pad) {
            return size.padStart(10, " ").replace(/ /g, "&nbsp;");
        }
        else{
            return size;
        }
    }
    function get_progress_speed(size, start_time, progress){
        var interval = (new Date()).getTime()/1000-start_time;
        var percentage = progress*100;
        var speed = size*progress/interval;
        return [percentage, speed];
    }
    function gen_progress(size, start_time, progress){
        var [percentage, speed] = get_progress_speed(size, start_time, progress);
        var eta = speed?size*(1-progress)/speed:-1;
        return "<div class='progress_wrapper'>" +
            "<div class='progress_bar' style='width: <percentage>%'></div><percentage>% (<speed>) (ETA: <eta>)</div>"
                .replace(/<percentage>/g, percentage.toFixed(2).padStart(6, " ").replace(/ /g, "&nbsp;"))
                .replace(/<eta>/g, (eta!==-1?Math.floor(eta/60).toString().padStart(2, " ")+"m "+Math.floor(eta%60).toString().padStart(2, " ")+"s":"unknown").replace(/ /g, "&nbsp;"))
                .replace(/<speed>/g, format_size(speed, 1)+"/s");
    }
    function convert_to_files(entries){
        var GB = 1024*1024*1024;
        var max_size = 10*GB;
        var total_size = 0;
        var skipped = 0;
        function check_file_size(file){
            let __b = !file.size||file.size>=max_size;
            if(!__b){
                total_size += file.size;
            }
            else{
                skipped += 1;
            }
            return __b;
        }
        function reader_progress(done) {
            if(done){
                info("Added "+fileEntries.length+" file(s) ("+format_size(total_size)+")<br/>Skipped: "+skipped+" file(s) (Too big or empty size)");
            }
            else{
                info("Adding files &#x22EF; ("+fileEntries.length+" file(s) queued)<br/>Please wait");
            }
        }
        var reader_ti = setInterval(reader_progress, 2000);
        var fileEntries = [];
        async function getAllFileEntries(dataTransferItemList) {
            let queue = [];
            for (let i = 0; i < dataTransferItemList.length; i++) {
                var _ = dataTransferItemList[i].webkitGetAsEntry();
                queue.push([(_.isDirectory?_.fullPath:"")+"/", _]);
            }
            while (queue.length > 0) {
                var [path, entry] = queue.shift();
                if (entry.isFile) {
                    var file = await fileEntryPromise(entry);
                    if(file) {
                        if (check_file_size(file)) {
                            continue;
                        }
                        file.path = path;
                        fileEntries.push(file);
                    }
                } else if (entry.isDirectory) {
                    var _ = await readAllDirectoryEntries(entry);
                    for(var i=0;i<_.length;i++) {
                        queue.push([(_[i].isDirectory?path+_[i].name+"/":path), _[i]]);
                    }
                }
            }
            return fileEntries;
        }
        async function readAllDirectoryEntries(directory) {
            let entries = [];
            let directoryReader = directory.createReader();
            while(1){
                let readEntries = await readEntriesPromise(directoryReader);
                if(!readEntries.length){
                    break;
                }
                for(var i=0;i<readEntries.length;i++) {
                    entries.push(readEntries[i]);
                }
            }
            return entries;
        }
        async function readEntriesPromise(directoryReader) {
            try {
                return await new Promise((resolve, reject) => {
                    directoryReader.readEntries(resolve, reject);
                });
            } catch (err) {
                return [];
            }
        }
        async function fileEntryPromise(fileEntry) {
            try {
                return await new Promise((resolve, reject) => {
                    fileEntry.file(resolve, reject);
                });
            } catch (err) {
                return null;
            }
        }
        return new Promise(function(resolve, reject){
            function next(what) {
                reader_progress(1);
                clearInterval(reader_ti);
                for (var i=0; i<what.length; i++){
                    what[i].overwrite = 0;
                }
                resolve(what);
            }
            if (entries instanceof FileList){
                for (var i=0; i<entries.length; i++){
                    if (check_file_size(entries[i])){
                        continue;
                    }
                    entries[i].path = "/";
                    fileEntries.push(entries[i]);
                }
                next(fileEntries);
            }
            else if (entries instanceof DataTransferItemList){
                getAllFileEntries(entries).then(next);
            }
        });
    }
    function update_file_drop_zone(_){
        if (!_.length) {
            return;
        }
        var file_drop_zone = $("div#file_drop_zone");
        for (var i=0;i<_.length;i++){
            _[i] = [_[i].name, _[i]];
        }
        file_drop_zone.removeClass("hint");
        files = files.concat(_);
        var template = "<tr class='file'>" +
            "<td class='name'><span title='Path<br/><i><path></i>'>&#x01F4C4; </span><name>" +
            "<span class='edit_name' title='Edit Name'>&#x270F;&#xFE0F;</span>" +
            "<span class='undo_edit' title='Undo Edit'>&#x21BA;</span>" +
            "</td>" +
            "<td class='size'><size></td>" +
            "<td class='overwrite' data-check='&#x2B1C;' data-checked='&#x2611;&#xFE0F;'>&#x2B1C;</td>" +
            "<td class='remove' title='Remove From Queue'>&#x26D4;</td>" +
            "</tr>";
        var table = "";
        table += "<table>";
        table += "<tr>" +
            "<th class='name' title='Remove From Queue<br/>Base On File Name'><span>&#x01F522;</span> File Name</th>" +
            "<th class='size' title='Remove From Queue<br/>Base On File Size'><span>&#x01F4D0;</span> File Size</th>" +
            "<th class='overwrite' title='Overwrite Existing File'><span>&#x2611;&#xFE0F;</span> Overwrite?</th>" +
            "<th class='remove'><span>&#x26D4;</span> Remove?</th>" +
            "</tr>";
        for (var i=0; i<files.length; i++){
            table += template
                .replace(/<path>/g, files[i][1].path)
                .replace(/<name>/g, files[i][0])
                .replace(/<size>/g, format_size(files[i][1].size));
        }
        table += "<tr class='file'><td colspan='4' id='choosemorefiles'>&#x01F4C2; Choose More Files &#x2795;</td></tr>";
        table += "</table>";
        file_drop_zone.empty().html(table);
        file_drop_zone.find("td#choosemorefiles").on("click", function () {
            $("form#upload_form input").get(0).click();
        });
        file_drop_zone.find("span.edit_name").on("click", function(){
            var file = files[file_drop_zone.find("span.edit_name").index(this)];
            var nn = prompt("Enter new name of '"+file[1].name+"':");
            if(!nn||file[0]===nn){
                return;
            }
            file[0] = nn;
            $(this).parent().contents()[1].data = nn;
            $(this).hide().next().show();
        });
        file_drop_zone.find("span.undo_edit").on("click", function(){
            var __file = files[file_drop_zone.find("span.undo_edit").index(this)];
            __file[0] = __file[1].name;
            $(this).parent().contents()[1].data = __file[1].name;
            $(this).hide().prev().show();
        }).hide();
        file_drop_zone.find("th.remove").on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            files.splice(1);
            file_drop_zone.find("td.remove").eq(0).trigger("click");
        });
        file_drop_zone.find("td.remove").on("click", function(e){
            e.preventDefault();
            e.stopPropagation();
            files.splice(file_drop_zone.find("td.remove").index(this), 1);
            if (!files.length){
                file_drop_zone.empty().addClass("hint");
                return;
            }
            $(this).closest("tr.file").remove();
        });
        file_drop_zone.find("th.size").on("click", function(){
            let filter_size = prompt("Examples:\nLarger than one gibibytes: > 1 GiB\nLess than or equal to one mebibytes: <=1mb\nEqual to one kibibyte: =1 kb\n\nEnter filter:").toLowerCase();
            let match;
            try{
                match = filter_size.match(/^(>=|<=|>|<|=) ?([0-9]+(?:\.[0-9]+)?) ?([kmgt])?i?[b]$/);
            }
            catch (e) {
                warning("Incorrect syntax: "+filter_size);
                return;
            }
            let eq = function (inte) {
                return inte === filter_size;
            }
            let gt = function (inte) {
                return inte > filter_size;
            }
            let lt = function (inte) {
                return inte < filter_size;
            }
            let ge = function (inte) {
                return inte >= filter_size;
            }
            let le = function (inte) {
                return inte <= filter_size;
            }
            let oper = match[1];
            if(oper===">"){
                oper = gt;
            }
            if(oper==="<"){
                oper = lt;
            }
            if(oper===">="){
                oper = ge;
            }
            if(oper==="<="){
                oper = le;
            }
            if(oper==="="){
                oper = eq;
            }
            filter_size = parseFloat(match[2]);
            let unit = match[3];
            if(unit==="t"){
                filter_size *= 1024;
                unit = "g";
            }
            if(unit==="g"){
                filter_size *= 1024;
                unit = "m";
            }
            if(unit==="m"){
                filter_size *= 1024;
                unit = "k";
            }
            if(unit==="k"){
                filter_size *= 1024;
            }
            file_drop_zone.find("table").hide();
            var tbr = file_drop_zone.find("td.remove").closest("tr.file");
            var __files = files;
            files = [];
            tbr = tbr.filter(function (i, e) {
                let file = __files[i];
                let r = oper(file[1].size);
                !r&&files.push(file);
                return r;
            });
            __files = null;
            tbr.remove();
            file_drop_zone.find("table").show();
            if (!files.length){
                file_drop_zone.empty().addClass("hint");
            }
        });
        file_drop_zone.find("th.overwrite").on("click", function(){
            var tds = file_drop_zone.find("td.overwrite");
            var tds2 = file_drop_zone.find("td.overwrite.checked");
            if(tds.length===tds2.length){
                tds2 = $();
            }
            file_drop_zone.find("table").hide();
            tds.not(tds2).map(function (i, e) {
                $(e).toggleClass("checked");
                $(e).html($(e).data("check"+($(e).hasClass("checked")?"ed":"")));
                var file = files[i];
                file[1].overwrite = !file[1].overwrite;
            });
            file_drop_zone.find("table").show();
        });
        file_drop_zone.find("td.overwrite").on("click", function(){
            $(this).toggleClass("checked");
            $(this).html($(this).data("check"+($(this).hasClass("checked")?"ed":"")));
            var file = files[file_drop_zone.find("td.overwrite").index(this)];
            file[1].overwrite = !file[1].overwrite;
        });
        update_scroll_hints($("div#pages"));
        update_title_hints();
        update_help_hints();
    }
    function gen_results(results){
        var templates = [
            ["<span>&#x01F4CB;</span> File List", 0, "<i><error><a href='<url>'><path><name></a><br/>"],
            ["<span>&#x01F517;</span> File Links", 1, "<url>\n"],
            ["[BBCode]", 1, "[URL=<url>]<name>[/URL]\n"],
            ["&lt;HTML Code&gt;", 1, "<a href='<url>' target='_blank'><name></a>\n"]
        ]
        var result = "";
        result += "<div class='upload_results'><div>";
        for (var j=0; j<templates.length; j++) {
            if (j===2){
                result += "</div><div>";
            }
            result += "<div class='upload_result' id='result"+j+"'>" + templates[j][0] + "</div>";
        }
        result += "</div></div>";
        for (var j=0; j<templates.length; j++) {
            if (!results.length){
                continue;
            }
            result += "<div class='result"+j+(j===0?" bordered_content":"")+"'>";
            if (templates[j][1]) {
                result += "<textarea>";
            }
            for (var i = 0; i < results.length; i++) {
                var error = "";
                // var integrity = results[i][2];
                // for (var k = 0; k < integrity.length; k++) {
                //     if (integrity[k][1][0] !== integrity[k][1][1]) {
                //         if (error){
                //             error += "<br/>";
                //         }
                //         error += "File "+ integrity[k][0] + " Integrity Check Failed";
                //     }
                // }
                // if (error){
                //     error = "<span title='"+error+"'>&#x26A0;&#xFE0F;</span> ";
                // }
                result += templates[j][2]
                    .replace(/<i>/g, (i+1)+". ")
                    .replace(/<error>/g, error)
                    .replace(/<url>/g, results[i][0])
                    .replace(/<path>/g, results[i][1])
                    // .replace(/<name>/g, results[i][2][0][1][0]);
                    .replace(/<name>/g, results[i][2]);
            }
            if (templates[j][1]) {
                result += "</textarea>";
            }
            result += "</div>";
        }
        return result;
    }
    $(document).on("dragover drop", function (e){
        e.preventDefault();
        if($("div#file_drop_zone table").length){
            $("div#file_drop_zone").removeClass("hint");
        }
    });
    $("div#file_drop_zone").on("dragover", function(e) {
        if (e.target === this) {
            e.stopPropagation();
            e.preventDefault();
            $(this).addClass("hint");
            e.originalEvent.dataTransfer.dropEffect = "copy";
        }
    }).on("drop", function(e) {
        if (e.target === this) {
            e.stopPropagation();
            e.preventDefault();
            convert_to_files(e.originalEvent.dataTransfer.items).then(update_file_drop_zone);
        }
    }).on("click", function(){
        if($(this).hasClass("hint")){
            $("form#upload_form input").get(0).click();
        }
    });
    $("form#upload_form input").on("change", function(){
        convert_to_files(this.files).then(update_file_drop_zone);
        this.value = "";
    });
    $("div#upload_again").on("click", function(){
        $("div#upload").trigger("click");
    });
	$("div#upload_btn").on("click", function () {
	    if (!files.length) {
            warning("Failed to upload file(s)<br/>Reason: No file(s)");
            return;
        }
	    $.post(api_endpoint, "op=get_upload_session", function (upload_session) {
	        $("div#toolbar").addClass("uploading");
            $("div#file_drop_zone").empty();
            $("div#file_drop_zone, div#upload_btn, div#upload_target").slideUp();
		    $("div#upload_progress, div#upload_results, div#upload_abort_btns").slideDown();
		    $("div#upload_results div").empty();
		    var results = [];
            function on_end(){
                $("div#toolbar").removeClass("uploading");
                if(!$("div#upload_results div").find("div.result0").length){
                    $("div#upload_results div").html("<h3>Upload probably failed.</h3><h3>File queue is processed.</h3>");
                }
                $("div#upload_progress, div#upload_abort_btns").slideUp();
                $("div#upload_again").slideDown(function () {
                    update_scroll_hints($("div#pages"));
                    update_title_hints();
                    update_help_hints();
                });
                info("Uploaded "+files.length+" file(s)");
                files = [];
                clear_cache();
            }
            function upload_file(index) {
                var _file = files[index];
                var file = files[index];
                if (!file) {
                    on_end();
                    return;
                }
                var filename = file[0];
                file = file[1];
                var sha256;
                var _ajax;
                var user_abort = 0;
                var session = gen_randstr();
                var start_time = (new Date()).getTime()/1000;
                var target_folder = [
                    $("div#upload_target select").find(":selected").data("name"),
                    parseInt($("div#upload_target select").val())
                ];
                var hash_flags = {"abort": 0};
                var query = [
                    ["op", "import_file"],
                    ["name", filename],
                    ["path", file.path],
                    ["size", file.size],
                    ["overwrite", file.overwrite?1:0]
                ];
                $("div#client td.hash").html("").parent().hide();
                $("div#client td.queue").html((index+1)+" out of "+files.length);
                $("div#client td.name").html(filename);
                $("div#client td.size").html(format_size(file.size)+" ("+file.size+" iB)");
                $("div#client td.progress").html(gen_progress(file.size, start_time, 0));
                $("div#upload_abort_btns").addClass("na").children().off("click").on("click", function () {
                    if($(this).attr("id")==="upload_abort_rest_btn") {
                        if(index+1>=files.length){
                            warning("Failed to abort rest.<br/>Reason: No rest to abort.")
                        }
                    }
                    if(!confirm("Are you sure to continue?")){
                        return;
                    }
                    if($(this).attr("id")==="upload_abort_rest_btn") {
                        success("Aborted "+files.splice(index+1).length+" file(s)");
                        return;
                    }
                    if($(this).attr("id")==="upload_abort_all_btn") {
                        user_abort = 1;
                    }
                    if($(this).attr("id")==="upload_abort_this_btn") {
                        if(index+1>=files.length){
                            user_abort = 1;
                        }
                        else {
                            user_abort = 2;
                        }
                    }
                    hash_flags["abort"] = user_abort;
                    _ajax.abort();
                });
                function show_results(__success) {
                    if(files.length&&(index+1>=files.length||(files.length<100&&__success))){
                        $("div#upload_results div").empty().html(gen_results(results));
                        $("div#upload_results textarea").each(function(){
                            CodeMirror.fromTextArea(this, {
                                "lineNumbers": true,
                                "lineWrapping": true,
                                "singleCursorHeightPerLine": false
                            });
                        });
                        $("div#upload_results div[id^='result']").map(function (i, el) {
                            $(el).on("click", function () {
                                $("div#upload_results div[class^='result']").hide();
                                $("div#upload_results div."+$(this).attr("id")).show();
                            });
                            if (i===0){
                                $(el).trigger("click");
                            }
                        });
                    }
                    else{
                        $("div#upload_results div").empty().html("<h3>Results are too big.</h3><h3>Please check after upload.</h3>");
                    }
                    update_scroll_hints($("div#pages"));
                    update_title_hints();
                    update_help_hints();
                }
                function _success(res, __success1, __success2) {
                    res = JSON.parse(res);
                    // var integrity = [
                    //     ["Name", [res["name"], filename]],
                    //     ["Size", [res["size"], file.size]]
                    //     // ["Hash", [res["hash"], sha256]]
                    // ];
                    results.push([
                        window.location.origin+"/"+res["id"],
                        (target_folder[0]==="root"?"":"/"+target_folder[0])+file.path,
                        filename
                        // integrity
                    ]);
                    success("Uploading &#x22EF; ("+(index+1)+"/"+files.length+")<br/>Uploaded file '"+filename+"'");
                    setTimeout(function(){
                        show_results(__success2);
                        _ajax = target_folder = file = filename = sha256 = session = query = done_ti = start_time = res = null;
                        _file.shift();
                        _file.shift();
                        upload_file(index+1);
                    }, __success1?1000:0);
                }
                function _error(e){
                    if(user_abort===1){
                        show_results(1);
                        on_end();
                        info("Aborted upload<br/>Uploaded "+index+" out of "+files.length+" file(s)");
                        return;
                    }
                    failure("Uploading &#x22EF; ("+(index+1)+"/"+files.length+")<br/>Failed to upload file '"+filename+"'");
                    file = filename = sha256 = session = query = start_time = null;
                    _file.shift();
                    _file.shift();
                    upload_file(index+1);
                }
                function proceed_upload(){
                    var local_progress_done = 0;
                    var form_data = new FormData();
                    form_data.append("sess_id", upload_session[1]);
                    form_data.append("file", file);
                    _ajax = $.ajax({
                        "xhr": function () {
                            var xhr = new window.XMLHttpRequest();
                            xhr.upload.addEventListener("progress", function (e) {
                                $("div#upload_abort_btns").removeClass("na");
                                if (e.lengthComputable&&!local_progress_done) {
                                    if(!local_progress_done) {
                                        local_progress_done = e.loaded === e.total;
                                    }
                                    $("div#client td.progress").html(gen_progress(file.size, start_time, e.loaded / e.total));
                                }
                            });
                            return xhr;
                        },
                        "type": "POST",
                        "url": upload_session[0],
                        "data": form_data,
                        "processData": false,
                        "contentType": false,
                        "success": function(r) {
                            var done_ti = setInterval(function () {
                                if (!sha256) {
                                    return;
                                }
                                if(!file.overwrite){
                                    query.push(["hash", sha256]);
                                }
                                clearInterval(done_ti);
                                query.push(["code", r[0]["file_code"]]);
                                for (var i=0;i<query.length;i++){
                                    query[i] = query[i][0]+"="+encodeURIComponent(query[i][1].toString());
                                }
                                query = query.join("&");
                                $.post(api_endpoint, query, function(response){
                                    _success(JSON.stringify(response), 1, 1);
                                }).error(_error);
                            }, 100);
                        },
                        "error": _error
                    });
                }
                function start_upload() {
                    // return proceed_upload();
                    // console.warn(new Date().getTime()/1000)
                    var _query = JSON.parse(JSON.stringify(query));
                    _query[0][1] = "check_file";
                    for (var i=0;i<_query.length;i++){
                        _query[i] = _query[i][0]+"="+encodeURIComponent(_query[i][1].toString());
                    }
                    _query = _query.join("&");
                    $.post(api_endpoint, _query, function(response) {
                        console.log(response)
                        if (response===null){
                            proceed_upload();
                        }
                        else{
                            hash_flags["abort"] = 2;
                            setTimeout(function () {
                                _success(JSON.stringify({"id": response}), 0, 1);
                            }, 50);
                        }
                    }).error(function(e){
                        hash_flags["abort"] = 2;
                        files = new Array(results.length);
                        show_results(1);
                        on_end();
                    });
                    // .error(function (e) {
                    //     // console.warn(new Date().getTime()/1000)
                    //     hash_flags["abort"] = 2;
                    //     if(e.status===409){
                    //         e = (e.responseText&&JSON.parse(e.responseText)["msg"])||"{}";
                    //         // sha256 = JSON.parse(e)["hash"];
                    //         setTimeout(function () {
                    //             _success(e, 0, 1);
                    //         }, 50);
                    //     }
                    //     else{
                    //         files = new Array(results.length);
                    //         show_results(1);
                    //         on_end();
                    //     }
                    // });
                }
                $("div#client td.hash").parent().show();
                var prev_hash_progress = 0;
                hash(file, hash_flags, function (progress) {
                    var hash_spd = file.size*progress/(new Date().getTime()/1000-start_time);
                    var hash_eta = file.size*(1-progress)/hash_spd;
                    $("div#client td.hash").html("Calculating &#x22EF; (<percentage>%) (<spd>/s) (ETA: <etam>m <etas>s)"
                        .replace("<percentage>", (progress*100).toFixed(2))
                        .replace("<spd>", format_size(hash_spd, 1))
                        .replace("<etam>", Math.floor(hash_eta/60).toString().padStart(" ", 2).replace(" ", "&nbsp;"))
                        .replace("<etas>", Math.floor(hash_eta%60).toString().padStart(" ", 2).replace(" ", "&nbsp;"))
                    );
                    prev_hash_progress = progress;
                }).then(function (_) {
                    sha256 = _;
                    $("div#client td.hash").html(sha256);
                    if (file.overwrite) {
                        query.push(["hash", sha256]);
                        start_upload();
                    }
                }, function (_) {
                    $("div#client td.hash").html((hash_flags["abort"]===1?"Failed":"Skipped")+" to calculate hash.");
                    setTimeout(function () {
                        _error(_);
                    }, 50);
                });
                if (!file.overwrite) {
                    start_upload();
                }
            }
            info("Uploading "+files.length+" file(s)");
            upload_file(0);
        }).error(function (e) {
            failure("Failed to upload.<br/>Reason: No upload session available");
        });
	    // return;
	    // if (!files.length) {
        //     warning("Failed to upload file(s)<br/>Reason: No file(s)");
        //     return;
        // }
	    // $("div#toolbar").addClass("uploading");
		// $("div#file_drop_zone").empty();
		// $("div#file_drop_zone, div#upload_btn, div#upload_target").slideUp();
		// $("div#upload_progress, div#upload_results, div#upload_abort_btns").slideDown();
		// $("div#upload_results div").empty();
		// var results = [];
        // function on_end(){
	    //     $("div#toolbar").removeClass("uploading");
        //     if(!$("div#upload_results div").find("div.upload_result").length){
        //         $("div#upload_results div").html("<h3>Upload probably failed.</h3><h3>File queue is processed.</h3>");
        //     }
        //     $("div#upload_progress, div#upload_abort_btns").slideUp();
        //     $("div#upload_again").slideDown(function () {
        //         update_scroll_hints($("div#pages"));
        //         update_title_hints();
        //         update_help_hints();
        //     });
        //     info("Uploaded "+files.length+" file(s)");
        //     files = [];
        //     clear_cache();
        // }
		// function upload_file(index) {
        //     var _file = files[index];
        //     var file = files[index];
        //     if (!file){
        //         on_end();
        //         return;
        //     }
        //     var filename = file[0];
        //     file = file[1];
        //     var sha256;
        //     var _ajax;
        //     var server_progress_ti;
        //     var server_progress_next;
        //     var user_abort = 0;
        //     var session = gen_randstr();
        //     var start_time = (new Date()).getTime()/1000;
        //     var target_folder = [
        //         $("div#upload_target select").find(":selected").data("name"),
        //         parseInt($("div#upload_target select").val())
        //     ];
        //     var hash_flags = {"abort": 0};
        //     var query = [
        //         ["session", session],
        //         ["folder", target_folder[1]],
        //         ["path", file.path],
        //         ["length", file.size]
        //     ];
        //     if(file.overwrite){
        //         query.push(["overwrite", "1"]);
        //     }
        //     for (var i=0;i<query.length;i++){
        //         query[i] = query[i][0]+"="+encodeURIComponent(query[i][1].toString());
        //     }
        //     query = query.join("&");
        //     var api_upload_url = api_endpoint+"/"+encodeURIComponent(filename)+"?"+query;
        //     $("div#client td.hash").html("").parent().hide();
        //     $("div#server td.cloned").html("Pending &#x22EF;");
        //     $("div#server td.uploaded").html("Pending &#x22EF;");
        //     $("div#client td.queue").html((index+1)+" out of "+files.length);
        //     $("div#client td.name").html(filename);
        //     $("div#client td.size").html(format_size(file.size)+" ("+file.size+" iB)");
        //     $("div#client td.progress").html(gen_progress(file.size, start_time, 0));
        //     $("div#server td.progress").html(gen_progress(file.size, start_time, 0));
        //     $("div#upload_abort_btns").addClass("na").children().off("click").on("click", function () {
        //         if($(this).attr("id")==="upload_abort_rest_btn") {
        //             if(index+1>=files.length){
        //                 warning("Failed to abort rest.<br/>Reason: No rest to abort.")
        //             }
        //         }
        //         if(!confirm("Are you sure to continue?")){
        //             return;
        //         }
        //         if($(this).attr("id")==="upload_abort_rest_btn") {
        //             success("Aborted "+files.splice(index+1).length+" file(s)");
        //             return;
        //         }
        //         if($(this).attr("id")==="upload_abort_all_btn") {
        //             user_abort = 1;
        //         }
        //         if($(this).attr("id")==="upload_abort_this_btn") {
        //             if(index+1>=files.length){
        //                 user_abort = 1;
        //             }
        //             else {
        //                 user_abort = 2;
        //             }
        //         }
        //         hash_flags["abort"] = 1;
        //         _ajax.abort();
        //     });
        //     function show_results(__success) {
        //         if(files.length&&(index+1>=files.length||(files.length<100&&__success))){
        //             $("div#upload_results div").empty().html(gen_results(results));
        //             $("div#upload_results textarea").each(function(){
        //                 CodeMirror.fromTextArea(this, {
        //                     "lineNumbers": true,
        //                     "lineWrapping": true,
        //                     "singleCursorHeightPerLine": false
        //                 });
        //             });
        //             $("div#upload_results div[id^='result']").map(function (i, el) {
        //                 $(el).on("click", function () {
        //                     $("div#upload_results div[class^='result']").hide();
        //                     $("div#upload_results div."+$(this).attr("id")).show();
        //                 });
        //                 if (i===0){
        //                     $(el).trigger("click");
        //                 }
        //             });
        //         }
        //         else{
        //             $("div#upload_results div").empty().html("<h3>Results are too big.</h3><h3>Please check after upload.</h3>");
        //         }
        //         update_scroll_hints($("div#pages"));
        //         update_title_hints();
        //         update_help_hints();
        //     }
        //     function server_progress() {
        //         if(server_progress_next){
        //             return;
        //         }
        //         server_progress_next = 1;
        //         $.post(api_endpoint, "op=get_relay_progress&session="+session, function(response){
        //             server_progress_next = 0;
        //             $("div#upload_abort_btns").removeClass("na");
        //             var _ = parseFloat(response)/100;
        //             $("div#server td.progress").html(gen_progress(file.size, start_time, _));
        //             if (_>=1) {
        //                 $("div#upload_abort_btns").addClass("na");
        //                 clearInterval(server_progress_ti);
        //                 $("div#server td.uploaded").html("&#x2B55; Done");
        //             }
        //         }).error(function (e) {
        //             console.warn(e.responseText);
        //             $("div#upload_abort_btns").addClass("na");
        //             if(JSON.parse(e.responseText)["msg"].indexOf("404")){
        //                 clearInterval(server_progress_ti);
        //                 _ajax.abort();
        //             }
        //             else{
        //                 server_progress_next = 0;
        //             }
        //         });
        //     }
        //     function _success(res, __success1, __success2) {
        //         res = JSON.parse(res);
        //         var integrity = [
        //             ["Name", [res["name"], filename]],
        //             ["Size", [res["size"], file.size]]
        //             // ["Hash", [res["hash"], sha256]]
        //         ];
        //         results.push([
        //             window.location.origin+"/"+res["id"],
        //             (target_folder[0]==="root"?"":"/"+target_folder[0])+file.path,
        //             integrity
        //         ]);
        //         var done_ti = setInterval(function () {
        //             // if (!sha256) {
        //             //     return;
        //             // }
        //             clearInterval(done_ti);
        //             clearInterval(server_progress_ti);
        //             success("Uploading &#x22EF; ("+(index+1)+"/"+files.length+")<br/>Uploaded file '"+filename+"'");
        //             $("div#server td.cloned").html("&#x2B55; Done");
        //             setTimeout(function(){
        //                 show_results(__success2);
        //                 _ajax = target_folder = file = filename = sha256 = session = query = done_ti = start_time = res = null;
        //                 _file.shift();
        //                 _file.shift();
        //                 upload_file(index+1);
        //             }, __success1?1000:0);
        //         }, __success1?1000:0);
        //     }
        //     function _error(e){
        //         clearInterval(server_progress_ti);
        //         if(user_abort===1){
        //             show_results(1);
        //             on_end();
        //             info("Aborted upload<br/>Uploaded "+index+" out of "+files.length+" file(s)");
        //             return;
        //         }
        //         failure("Uploading &#x22EF; ("+(index+1)+"/"+files.length+")<br/>Failed to upload file '"+filename+"'");
        //         $("div#server td.uploaded").html("&#x274C; Failed");
        //         file = filename = sha256 = session = query = start_time = null;
        //         _file.shift();
        //         _file.shift();
        //         upload_file(index+1);
        //     }
        //     function proceed_upload(){
        //         var local_progress_done = 0;
        //         _ajax = $.ajax({
        //             "xhr": function () {
        //                 if(!server_progress_ti) {
        //                     server_progress_ti = setInterval(server_progress, 1000);
        //                 }
        //                 var xhr = new window.XMLHttpRequest();
        //                 xhr.upload.addEventListener("progress", function (e) {
        //                     if (e.lengthComputable&&!local_progress_done) {
        //                         if(!local_progress_done) {
        //                             local_progress_done = e.loaded === e.total;
        //                         }
        //                         $("div#client td.progress").html(gen_progress(file.size, start_time, e.loaded / e.total));
        //                     }
        //                 });
        //                 return xhr;
        //             },
        //             "type": "POST",
        //             "url": api_upload_url+(sha256?"&hash="+sha256:""),
        //             "data": new Blob([file], {type: "application/octet-stream"}),
        //             "processData": false,
        //             "contentType": false,
        //             "success": function(r) {
        //                 _success(r, 1, 1);
        //             },
        //             "error": _error
        //         });
        //     }
        //     function start_upload() {
        //         // console.warn(new Date().getTime()/1000)
        //         $.ajax({
        //             "type": "GET",
        //             "url": api_upload_url+(sha256?"&hash="+sha256:""),
        //             "success": function(response) {
        //                 proceed_upload();
        //             },
        //             "error": function (e) {
        //                 // console.warn(new Date().getTime()/1000)
        //                 if(e.status===409){
        //                     e = (e.responseText&&JSON.parse(e.responseText)["msg"])||"{}";
        //                     // sha256 = JSON.parse(e)["hash"];
        //                     setTimeout(function () {
        //                         _success(e, 0, 1);
        //                     }, 50);
        //                 }
        //                 else{
        //                     files = new Array(results.length);
        //                     show_results(1);
        //                     on_end();
        //                 }
        //             }
        //         });
        //     }
        //     if (file.overwrite) {
        //         $("div#client td.hash").parent().show();
        //         var prev_hash_progress = 0;
        //         hash(file, hash_flags, function (progress) {
        //             var hash_spd = file.size*progress/(new Date().getTime()/1000-start_time);
        //             var hash_eta = file.size*(1-progress)/hash_spd;
        //             $("div#client td.hash").html("Calculating &#x22EF; (<percentage>%) (<spd>/s) (ETA: <etam>m <etas>s)"
        //                 .replace("<percentage>", (progress*100).toFixed(2))
        //                 .replace("<spd>", format_size(hash_spd, 1))
        //                 .replace("<etam>", Math.floor(hash_eta/60).toString().padStart(" ", 2).replace(" ", "&nbsp;"))
        //                 .replace("<etas>", Math.floor(hash_eta%60).toString().padStart(" ", 2).replace(" ", "&nbsp;"))
        //             );
        //             prev_hash_progress = progress;
        //         }).then(function (_) {
        //             sha256 = _;
        //             $("div#client td.hash").html(sha256);
        //             start_upload();
        //         }, function (_) {
        //             $("div#client td.hash").html((hash_flags["abort"]===1?"Failed":"Skipped")+" to calculate hash.");
        //             setTimeout(function () {
        //                 _error(_);
        //             }, 50);
        //         });
        //     }
        //     else{
        //         start_upload();
        //     }
        // }
        // info("Uploading "+files.length+" file(s)");
        // upload_file(0);
	});
    window.onhashchange = function () {
        var hash = window.location.hash.slice(1);
        if(hash.indexOf("folder=")!==-1){
            return get_folders(hash.slice(7), 1);
        }
        else if(hash==="main"){
            $("div#main").trigger("click");
        }
        else if(hash==="upload"){
            $("div#tools div#upload").trigger("click");
        }
        else if(hash==="files"){
            $("div#tools div#files").trigger("click");
        }
        else if(hash==="import"){
            $("div#tools div#import").trigger("click");
        }
        else if(hash==="import2"){
            $("div#tools div#import2").trigger("click");
        }
    }
    var id = window.location.pathname.slice(1);
    if(id){
        function next() {
            $("div#file_page").show();
            $("div#pages").slideDown(function () {
                update_scroll_hints($("div#pages"));
                update_title_hints();
                update_help_hints();
            });
            var dl_btn = $("a#dl_btn");
            var dl_link = $("a#dl_link");
            var _ = [dl_btn.html(), dl_link.html()];
            dl_link.html(dl_link.data("clone"));
            dl_btn.html(dl_btn.data("clone"));
            info("Getting file '" + id + "'");
            $.post(api_endpoint, "op=get_file&id=" + id, function (response) {
                var mimetype = mimeType.lookup(response[0]["name"])||"";
                if (mimetype) {
                    var mime_map = {
                        "application": "&#x2699;&#xFE0F;",
                        "audio": "&#x01F3B5;",
                        "font": "&#x01D4D0;&#x01D4B6;",
                        "image": "&#x01F5BC;&#xFE0F;",
                        "model": "&#x01F54B;",
                        "video": "&#x01F39E;&#xFE0F;",
                    };
                    mimetype = mime_map[mimetype.split("/")[0]];
                }
                $("div#file_type").html(mimetype || "");
                $("div#file_name").html(response[0]["name"]);
                $("div#file_size").html(format_size(response[0]["size"]));
                $("div#file_hash").html(response[0]["hash"]);
                $("div#file_date").html(response[0]["date"]);
                info("Cloning file '" + id + "'");
                $.post(api_endpoint, "op=clone_file&id=" + id, function (response) {
                    dl_link.addClass("ready").attr("href", response).html(dl_link.data("ready"));
                    dl_btn.html(dl_btn.data("fetch")).addClass("fetch");
                    info("Getting download link '" + response + "'");
                    $.get(window.location.origin.replace("ucefc.", "resolve.ucefc.")+"/"+response.split("/").slice(-1)[0], function (response) {
                        dl_btn.attr("href", response).addClass("ready").html(dl_btn.data("ready"));
                        success("Download link ready");
                    }).error(function (e) {
                        dl_btn.removeClass("fetch").html(_[0]);
                        failure("Failed to get download link<br/>Try \"File Link\" instead");
                    });
                }).error(function (e) {
                    dl_btn.html(_[0]);
                    dl_link.html(_[1]);
                    failure("Failed to clone file<br/>Reason: " + e.responseText);
                });
            }).error(function (e) {
                failure("Failed to get file<br/>Reason: File does not exist");
                dl_btn.html(_[0]);
                dl_link.html(_[1]);
            });
        }
        $("div#main").addClass("done");
        var l = $("div#toolbar").width() - $("div#main").width() - $("div#tools").outerWidth();
        if (l > $("div#tools").outerWidth(true) - $("div#tools").outerWidth()) {
            $("div#tools").addClass("done").animate({"margin-left": l}, 333, next);
        }
        else{
            next();
        }
    }
    else if (cur_folder){
        if (!window.location.pathname.slice(1)) {
            function next() {
                $("div#files_page").show();
                $("div#pages").slideDown(function () {
                    update_scroll_hints($("div#pages"));
                    update_title_hints();
                });
                window.onhashchange();
            }
            $("div#main").addClass("done");
            var l = $("div#toolbar").width() - $("div#main").width() - $("div#tools").outerWidth();
            if (l > $("div#tools").outerWidth(true) - $("div#tools").outerWidth()) {
                $("div#tools").addClass("done").animate({"margin-left": l}, 333, next);
            }
            else{
                next();
            }
        }
    }
    if(["main", "files", "upload", "import", "import2"].indexOf(window.location.hash.slice(1))!==-1){
        window.onhashchange();
    }
}
$("title").attr("data-html", $("title").html());
$("div#toolbar").hide();
$.ajaxSetup({
    "complete": function(){
        notlogin = document.cookie.indexOf("session=") === -1;
        if(!notlogin_o&&notlogin!==notlogin_o){
            alert("We don't know how but\nyou did something unauthorized\nreloading now");
            window.location.reload();
        }
    }
});
function resize(a){
    var div_tools_margin_left = $("div#tools").outerWidth(true) - $("div#tools").outerWidth();
    return function() {
        if (a) {
            var l = $("div#toolbar").width() - $("div#main").width() - $("div#tools").outerWidth();
            if (l > div_tools_margin_left) {
                $("div#tools").addClass("done").css({"margin-left": l});
            }
        }
        if ($(this).width() >= $(this).height()) {
            $("body").addClass("toggle");
        } else {
            $("body").removeClass("toggle");
        }
    }
}
$(window).on("resize", resize(1));
resize().apply($(window));
var api_endpoint = window.location.origin+"/api";
var notlogin = document.cookie.indexOf("session=") === -1;
var notlogin_o = document.cookie.indexOf("session=") === -1;
var bg_img = "https://foxe6.github.io/BLOG/img/asset/orange_polygon_star.";
$("body").css("background-image", "url('" + bg_img + (is_mobile?"jpg":"png") + "')");
$(document).on("ready", function(){
    $("div#loading").remove();
    if(!notlogin){
        $("div#tools div#login").remove();
        $("div#pages div#login_page").remove();
        $("div#upload_page div#notlogin").remove();
    }
    else{
        $("div#tools div#logout, div#pages div#files_page div#file_ops, div#files_page div#goto_import, div#files_page div#goto_import2").remove();
        $("div#upload_page").children().not("div#notlogin").remove();
    }
    setup_scroll_hints($("div#pages"));
    $("div#toolbar").fadeIn(666, function(){
        $("div#pages > div[id]").hide();
        if(!window.location.pathname.slice(1)&&!window.location.hash.slice(1)) {
            main();
            window.location.hash = "main";
        }
        else{
            main();
        }
    });
});
