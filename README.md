
## Saamfram Protocol Design Goals:
* Group Communication of Forms: Produce a data efficient protocol for sending forms to multiple stations simultaneously in a group setting with efficient round robin verification and re-transmit process. Protocol supports Peer to Peer, Peer to Group, Group to Peer and Group to Group.
* Critical Messages: Enables transfer of fully verified, error-corrected emails/forms/messages in real time.
* Notifications: Provide an efficient mechanism for group notification of any pending messages waiting to be sent out.
* Flexibility: Incorporate multiple message delivery techniques including push, pull, store and forward, relay, active session, passive mode.
* Content Only: Separate out the pre-existing form information such as form layout and text field information from the form content thus significantly reducing the amount of data that needs to be sent with any ICS form message transfer. Content only delivery of forms reduces message length significantly and increases performance, reliability and resilience.
* Data Compression: Run Length Encoding is used for content data and Dictionary Compression for form templates. These techniques significantly reduce the amount of data that needs to be transmitted when sending forms. This provides an additional reduction to the average message length and further increases performance, reliability and resilience.
* Increased Performance and Resilience: Multiple techniques have been incorporated. When used in combination, these provide a highly accurate and efficient RF data transfer mode that can be used with a variety of digital modes and Ham Radio bands including the lower HF bands (160/80/60/40/30m) where reliable communication can be problematic.
* When used in conjunction with JS8/JS8Call it is also possible to receive form transmissions passively from multiple stations simultaneously. These capabilites make it possible to send form messages Peer to Peer, Peer to Group, Group to Peer and Group to Group. These capabilities provide the basis for a new set of tools for ham radio operators to complement the existing Peer to Peer and Peer to Gateway approaches. 


## Copyright/License

MIT License

Copyright (c) 2022 Lawrence Byng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


