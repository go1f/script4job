function hash(e, t) {
var n = (new Date).getTime().toString().substring(0, 10),
r = bo(n + e + t);
return {
time: n,
passwd: r
}
}
var vo = 0;
function bo(e) {
return yo(_o(wo(e)))
}
function _o(e) {
return xo(Mo(Co(e), 8 * e.length))
}
function yo(e) {
for (var t, n = vo ? '0123456789ABCDEF' : '0123456789abcdef', r = '', i = 0; i < e.length; i++) t = e.charCodeAt(i),
r += n.charAt(t >>> 4 & 15) + n.charAt(15 & t);
return r
}
function wo(e) {
var t,
n,
r = '',
i = - 1;
while (++i < e.length) t = e.charCodeAt(i),
n = i + 1 < e.length ? e.charCodeAt(i + 1)  : 0,
55296 <= t && t <= 56319 && 56320 <= n && n <= 57343 && (t = 65536 + ((1023 & t) << 10) + (1023 & n), i++),
t <= 127 ? r += String.fromCharCode(t)  : t <= 2047 ? r += String.fromCharCode(192 | t >>> 6 & 31, 128 | 63 & t)  : t <= 65535 ? r += String.fromCharCode(224 | t >>> 12 & 15, 128 | t >>> 6 & 63, 128 | 63 & t)  : t <= 2097151 && (r += String.fromCharCode(240 | t >>> 18 & 7, 128 | t >>> 12 & 63, 128 | t >>> 6 & 63, 128 | 63 & t));
return r
}
function Co(e) {
for (var t = Array(e.length >> 2), n = 0; n < t.length; n++) t[n] = 0;
for (n = 0; n < 8 * e.length; n += 8) t[n >> 5] |= (255 & e.charCodeAt(n / 8)) << 24 - n % 32;
return t
}
function xo(e) {
for (var t = '', n = 0; n < 32 * e.length; n += 8) t += String.fromCharCode(e[n >> 5] >>> 24 - n % 32 & 255);
return t
}
function So(e, t) {
return e >>> t | e << 32 - t
}
function Bo(e, t) {
return e >>> t
}
function ko(e, t, n) {
return e & t ^ ~e & n
}
function Eo(e, t, n) {
return e & t ^ e & n ^ t & n
}
function To(e) {
return So(e, 2) ^ So(e, 13) ^ So(e, 22)
}
function Io(e) {
return So(e, 6) ^ So(e, 11) ^ So(e, 25)
}
function Fo(e) {
return So(e, 7) ^ So(e, 18) ^ Bo(e, 3)
}
function Do(e) {
return So(e, 17) ^ So(e, 19) ^ Bo(e, 10)
}
var No = new Array(1116352408, 1899447441, - 1245643825, - 373957723, 961987163, 1508970993, - 1841331548, - 1424204075, - 670586216, 310598401, 607225278, 1426881987, 1925078388, - 2132889090, - 1680079193, - 1046744716, - 459576895, - 272742522, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, - 1740746414, - 1473132947, - 1341970488, - 1084653625, - 958395405, - 710438585, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, - 2117940946, - 1838011259, - 1564481375, - 1474664885, - 1035236496, - 949202525, - 778901479, - 694614492, - 200395387, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, - 2067236844, - 1933114872, - 1866530822, - 1538233109, - 1090935817, - 965641998);
function Mo(e, t) {
var n,
r,
i,
a,
o,
s,
l,
c,
u,
d,
h,
f,
p = new Array(1779033703, - 1150833019, 1013904242, - 1521486534, 1359893119, - 1694144372, 528734635, 1541459225),
A = new Array(64);
for (e[t >> 5] |= 128 << 24 - t % 32, e[15 + (t + 64 >> 9 << 4)] = t, u = 0; u < e.length; u += 16) {
for (n = p[0], r = p[1], i = p[2], a = p[3], o = p[4], s = p[5], l = p[6], c = p[7], d = 0; d < 64; d++) A[d] = d < 16 ? e[d + u] : Oo(Oo(Oo(Do(A[d - 2]), A[d - 7]), Fo(A[d - 15])), A[d - 16]),
h = Oo(Oo(Oo(Oo(c, Io(o)), ko(o, s, l)), No[d]), A[d]),
f = Oo(To(n), Eo(n, r, i)),
c = l,
l = s,
s = o,
o = Oo(a, h),
a = i,
i = r,
r = n,
n = Oo(h, f);
p[0] = Oo(n, p[0]),
p[1] = Oo(r, p[1]),
p[2] = Oo(i, p[2]),
p[3] = Oo(a, p[3]),
p[4] = Oo(o, p[4]),
p[5] = Oo(s, p[5]),
p[6] = Oo(l, p[6]),
p[7] = Oo(c, p[7])
}
return p
}
function Oo(e, t) {
var n = (65535 & e) + (65535 & t),
r = (e >> 16) + (t >> 16) + (n >> 16);
return r << 16 | 65535 & n
}

function go(e, t) {
var n = (new Date).getTime().toString().substring(0, 10),
r = bo(n + e + t);
return {
time: n,
passwd: r
}
}


go(1,2)