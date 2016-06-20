followers_pp = None
followers_psoe = None
followers_podemos = None
followers_cs = None


# FIRST FOLLOWERS SNAPSHOT: JUNE 15 2016

if __name__ == '__main__':
    with open("PPopular.txt", 'r') as file_pp:
        followers_pp = file_pp.readlines()

    with open("PSOE.txt", 'r') as file_psoe:
        followers_psoe = file_psoe.readlines()

    with open("ahorapodemos.txt", 'r') as file_podemos:
        followers_podemos = file_podemos.readlines()

    with open("CiudadanosCs.txt", 'r') as file_cs:
        followers_cs = file_cs.readlines()

    print len(followers_pp)
    print len(followers_psoe)
    print len(followers_podemos)
    print len(followers_cs)

    followers_pp_psoe = list(set(followers_pp) & set(followers_psoe))
    followers_pp_cs = list(set(followers_pp) & set(followers_cs))
    followers_pp_podemos = list(set(followers_pp) & set(followers_podemos))
    followers_psoe_cs = list(set(followers_psoe) & set(followers_cs))
    followers_psoe_podemos = list(set(followers_psoe) & set(followers_podemos))
    followers_cs_podemos = list(set(followers_cs) & set(followers_podemos))

    followers_all = list(set(followers_pp) & set(followers_psoe) & set(followers_cs) & set(followers_podemos))

    print "PP - PSOE"
    print str((len(followers_pp_psoe) * 100) / len(followers_pp)) + "% of PP's followers are also PSOE's followers"
    print "PSOE - PP"
    print str((len(followers_pp_psoe) * 100) / len(followers_psoe)) + "% of PSOE's followers are also PP's followers"

    print "PP - Cs"
    print str((len(followers_pp_cs) * 100) / len(followers_pp)) + "% of PP's followers are also Cs's followers"
    print "Cs - PP"
    print str((len(followers_pp_cs) * 100) / len(followers_cs)) + "% of Cs's followers are also PP's followers"

    print "PSOE - Podemos"
    print str((len(followers_psoe_podemos) * 100) / len(followers_psoe)) + "% of PSOE's followers are also Podemos's followers"
    print "Podemos - PSOE"
    print str((len(followers_psoe_podemos) * 100) / len(followers_podemos)) + "% of Podemos's followers are also PSOE's followers"

    print "PP - Podemos"
    print str((len(followers_pp_podemos) * 100) / len(followers_pp)) + "% of PP's followers are also Podemos's followers"
    print "Podemos - PP"
    print str((len(followers_pp_podemos) * 100) / len(followers_podemos)) + "% of Podemos's followers are also PP's followers"

    print "PSOE - Cs"
    print str((len(followers_psoe_cs) * 100) / len(followers_psoe)) + "% of PSOE's followers are also Cs's followers"
    print "Cs - PSOE"
    print str((len(followers_psoe_cs) * 100) / len(followers_cs)) + "% of Cs's followers are also PSOE's followers"

    print "Podemos - Cs"
    print str((len(followers_cs_podemos) * 100) / len(followers_podemos)) + "% of Podemos's followers are also Cs's followers"
    print "Cs - Podemos"
    print str((len(followers_cs_podemos) * 100) / len(followers_cs)) + "% of Cs's followers are also Podemos's followers"

    print len(followers_pp_psoe)
    print len(followers_pp_cs)
    print len(followers_pp_podemos)
    print len(followers_psoe_cs)
    print len(followers_psoe_podemos)
    print len(followers_cs_podemos)
    print len(followers_all)
