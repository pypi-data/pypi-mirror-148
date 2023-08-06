# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import base64, codecs
magic = 'IyBQYXJ0IG9mIHRoZSBST0JPSUQgcHJvamVjdCAtIGh0dHA6Ly9oYW1zdGVyLnNjaG9vbAojIENvcHlyaWdodCAoQykgMjAxNiBLd2FuZy1IeXVuIFBhcmsgKGFrYWlpQGt3LmFjLmtyKQojIAojIFRoaXMgbGlicmFyeSBpcyBmcmVlIHNvZnR3YXJlOyB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3IKIyBtb2RpZnkgaXQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBHTlUgTGVzc2VyIEdlbmVyYWwgUHVibGljCiMgTGljZW5zZSBhcyBwdWJsaXNoZWQgYnkgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbjsgZWl0aGVyCiMgdmVyc2lvbiAyLjEgb2YgdGhlIExpY2Vuc2UsIG9yIChhdCB5b3VyIG9wdGlvbikgYW55IGxhdGVyIHZlcnNpb24uCiMgCiMgVGh'
love = 'cplOfnJWlLKW5VTymVTEcp3ElnJW1qTIxVTyhVUEbMFObo3OyVUEbLKDtnKDtq2yfoPOvMFO1p2IzqJjfPvZtLaI0VSqWIRuCIIDtDH5MVSqOHyWOGyEMBlO3nKEbo3I0VTI2MJ4tqTuyVTygpTkcMJDtq2SlpzShqUxto2LXVlOAEIWQFRSBIRSPFHkWISxto3VtExyHGxIGHlOTG1VtDFODDIWHFHAIGRSFVSOIHyOCH0HhVPOGMJHtqTuyVRqBIDbwVRkyp3AypvOUMJ5ypzSfVSO1LzkcLlOZnJAyoaAyVTMipvOgo3WyVTEyqTScoUZhPvZtPvZtJJ91VUAbo3IfMPObLKMyVUWyL2IcqzIxVTRtL29jrFOiMvO0nTHtE05IVRkyp3AypvOUMJ5ypzSfPvZtHUIvoTywVRkcL2Ihp2HtLJkiozptq2y0nPO0nTymVTkcLaWupax7VTyzVT5iqPjtq3WcqTHtqT8tqTuyPvZtEa'
god = 'JlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uLCBJbmMuLCA1OSBUZW1wbGUgUGxhY2UsIFN1aXRlIDMzMCwKIyBCb3N0b24sIE1BICAwMjExMS0xMzA3ICBVU0EKCmZyb20gcm9ib2lkIGltcG9ydCB3YWl0CmZyb20gcm9ib2lkYWkuX2tleWV2ZW50IGltcG9ydCBLZXlFdmVudApmcm9tIHB5bnB1dC5rZXlib2FyZCBpbXBvcnQgS2V5CgoKX0tFWV9UT19DT0RFUyA9IHsKICAgICdicyc6IEtleS5iYWNrc3BhY2UsCiAgICAndGFiJzogS2V5LnRhYiwKICAgICdlbnRlcic6IEtleS5lbnRlciwKICAgICdlc2MnOiBLZXkuZXNjLAogICAgJyAnOiBLZXkuc3BhY2UKfQoKCmRlZiB3YWl0X3VudGlsX2tleShrZXk9Tm9uZSk6CiAgICBpZiBpc2luc3RhbmNlKGtleSwgc3RyK'
destiny = 'GbXVPNtVPNtVPOfo3qsn2I5VQ0tn2I5Yzkiq2IlXPxXVPNtVPNtVPOcMvOfo3qsn2I5VTyhVS9YEIysIR9sD09REIZ6PvNtVPNtVPNtVPNtVTgyrFN9VS9YEIysIR9sD09REIAooT93K2gyrI0XVPNtVRgyrHI2MJ50YaA0LKW0XPxXVPNtVUqbnJkyVSElqJH6PvNtVPNtVPNtnJLtn2I5VTymVR5iozH6PvNtVPNtVPNtVPNtVTyzVRgyrHI2MJ50YzqyqS9lMJkyLKAyMS9eMKxbXFOcplOho3DtGz9hMGbXVPNtVPNtVPNtVPNtVPNtVTWlMJSePvNtVPNtVPNtMJkmMGbXVPNtVPNtVPNtVPNtnJLtF2I5EKMyoaDhM2I0K3WyoTIup2IxK2gyrFtcVQ09VTgyrGbXVPNtVPNtVPNtVPNtVPNtVTWlMJSePvNtVPNtVPNtq2ScqPtlZPxXVPNtVRgyrHI2MJ50YaA0o3NbXDb='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))