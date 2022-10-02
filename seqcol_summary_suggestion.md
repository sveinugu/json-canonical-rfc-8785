# Suggestion: supporting ChrLens through summary arrays

So one of the use cases sequence collections aims to solve is for it to be able to provide coordinate systems in the 
form of ordered `(name, lenght)` pairs. The way that we are currently thinking of supporting this is to make the  
`sequences` array optional to allow the possibility of implementations that contain coordinate systems rather than 
full sequence collections. While this seems like a nice solution in theory, I think in practice it would have some  
limitations:

  - This solution implies that since a coordinate system can be represented by the seqcol standard, a coordinate 
    system  is actually a type of sequence collection. But a coordinate system is very clearly is not a sequence 
    collection as it does not collect any sequences! So as a minimum, we have a naming problem. However, in my 
    experience, if you are unable to properly name your object then perhaps that is an indication that your model 
    is wrong.

This issue is not just about semantics, it has practical consequences. A scenario to illustrate:

Given:
  - BED file A generated on the basis of a reference genome with seqcol digest SD[A] 
  - BED file B generated on the basis of a different reference genome with seqcol digest SD[B] 
  - SCHBEDtools, a BEDtools-like tool that has support for taking seqcol digests as input instead of ChromLen files
  - A workflow of two steps:
    - Step 1:
      - Input: files A and B with seqcol digests SD[A] and SD[B] as parameters. 
      - Output: new BED file C + a seqcol digest CS[C] representing a coordinate system
    - Step 2:
      - Input: file C with seqcol digest CS[C] representing a coordinate system as parameter
      - Output: new BED file D + a seqcol digest CS[D] representing a coordinate system
  - Notes:
    - CS[C] represents a coordinate system of the sequences that are found in both A and B, based on the `names` and  
      `lengths` arrays only, excluding the `sequences`
    - CS[C] == CS[D] (which is easy to see directly from the digests - a pragmatically useful detail)

Question:
  - Will we with the current solution support such a scenario, if not directly, at least in a way that makes this 
    easy to implement by a third party?

Advantages:
  - One advantage to this is that representing a coordinate system with a digest makes workflows like the 
    one above easier to manage in a practical sense. 
  
  - A more important advantage is that a coordinate system digest can be persisted as a metadata variable directly 
    connected to the files (which is relatively easy to do), as part of FAIR management of metadata on research 
    analyses. The alternative is to instead have to maintain a reference to a separate ChromLen file (which is a 
    bother and consequently easy to drop)  

Possible implementation
  - Implementing step 1 in SCHBEDtools:
    1. Contact one or more seqcol servers with the digests SD[A] and SD[B] and receive the full array contents.
    2. Keep only the `names` and `lengths` arrays, discard the rest (including `sequences`)
    3. Find which `(name, length)` pairs are in both collections. This set is NLP[AB]
    4. Order NLP according to, say, A
    5. Generate a seqcol digest CS[C] based on the ordered NLP[AB]
    6. Carry out the rest of the step, using CS[C] as basis for the joint coordinate system

  - So far, so good. Seqcol has definitely helped a lot!

  - Implementing step 2 in SCHBEDtools (Here we assume no other information is kept from step 1 other than the inputs):
    1. Try the standard servers using the digest CS[C], but no results
    2. Try a third-party implementation of a seqcol server for coordinate systems. However, int this example, CS[C] 
       does not directly match a single entry, as the exact list of sequences in the order specificed by A are a bit 
       different than the sequence collections that were fed into the server. Having an unordered seqcol digest would 
       have helped a lot to reduce the search space, but the exact list of sequences might still be a bit off from 
       any of the registered seqcols.
    3. Cry SCHBED-tears!

Problems:
  - Before going into the details on how to solve this, I think one of the major issues with the current idea for 
    coordinate system support is that is requires third-parties to set up and maintain servers for coordinate 
    systems. Since we are then talking mostly about researchers, there will be problems with long-term maintenance. 
    After some years, the coordinate system servers get outdated and other competing ones start up, however these 
    also gets outdated, and so on.
  - Having coordinate system support in the main seqcol standard that are to be adopted by the major databases would 
    be a much more robust solution

Solutions:
  - So the third-party coordinate system server could have fixed the issue by generating digests for all possible 
    permutations of sequences. This will be a much easier task if we are talking about unordered digests. But in any 
    case it looks more like a hack.
  - SCHBED-tools could opt for limiting itself to the priority sequences and only move forward if these were the 
    same in SC[A] and SC[B]. This requires that a) we do provide the priority bits (or something similar), and b) 
    canonical ordering would still be useful. However this restriction might be a bit too strict for certain usage 
    scenarios, and still feels a bit like a hack.
  - SCHBED-tools could have registered CS[C] in a server as part of Step 1. 

Idea:
  - Add summary arrays to the current seqcol implementation. The set of summary arrays follow exactly the same rules 
    and data structures as the reqular seqcol. The only difference is the values and contents, possibly also in the 
    digest algorithm if we want unordered digests.

Example sequence collection:

"c49b1c24" = '{"lengths":"a6027583","names":"48c4f4d9","sequences":"932793b3"}' + '{"chrlen":"0841a2f7,
"das":"0841a2f7","udas":"ff5e7c82","chrlenpri1":"34dbc45a"'}

c49b1c24 - a84fee0a

| names | lengths | sequences |priority
|-------|---------|-----------|
| chr1  | 12345   | 96f04ea2c |1
| chr2  | 23456   | 00330e995 |1
| chr3  | 34567   | 572853213 |2

Example summary arrays

|          names-lengths           |             lengths-sequences             |
|:--------------------------------:|:-----------------------------------------:|
| {"names":"chr1","lengths":12345} | {"lengths":12345,"sequences":"96f04ea2c"} |
| {"names":"chr2","lengths":23456} | {"lengths":23456,"sequences":"00330e995"} |
| {"names":"chr3","lengths":34567} | {"lengths":34567,"sequences":"572853213"} |


|          names-lengths           |             lengths-sequences             |
|:--------------------------------:|:-----------------------------------------:|
|             32678dcb             | {"lengths":12345,"sequences":"96f04ea2c"} |
| {"names":"chr2","lengths":23456} | {"lengths":23456,"sequences":"00330e995"} |
| {"names":"chr3","lengths":34567} | {"lengths":34567,"sequences":"572853213"} |