import torch
import torch.nn as tnn
import re
import dill
from torchtext import data
#stop words
stop_words = ["a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren",
              "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
              "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing",
              "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has",
              "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him",
              "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself",
              "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself",
              "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other",
              "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's",
              "should", "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll",
              "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those",
              "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were",
              "weren", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with",
              "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
              "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm",
              "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", "they're",
              "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would",
              "able", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj",
              "affected", "affecting", "affects", "afterwards", "ah", "almost", "alone", "along", "already", "also",
              "although", "always", "among", "amongst", "announce", "another", "anybody", "anyhow", "anymore", "anyone",
              "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "arent", "arise", "around",
              "aside", "ask", "asking", "auth", "available", "away", "awfully", "b", "back", "became", "become",
              "becomes", "becoming", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "believe",
              "beside", "besides", "beyond", "biol", "brief", "briefly", "c", "ca", "came", "cannot", "can't", "cause",
              "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains",
              "couldnt", "date", "different", "done", "downwards", "due", "e", "ed", "edu", "effect", "eg", "eight",
              "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "etc", "even",
              "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "ff",
              "fifth", "first", "five", "fix", "followed", "following", "follows", "former", "formerly", "forth",
              "found", "four", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving",
              "go", "goes", "gone", "got", "gotten", "h", "happens", "hardly", "hed", "hence", "hereafter", "hereby",
              "herein", "heres", "hereupon", "hes", "hi", "hid", "hither", "home", "howbeit", "however", "hundred",
              "id", "ie", "im", "immediate", "immediately", "importance", "important", "inc", "indeed", "index",
              "information", "instead", "invention", "inward", "itd", "it'll", "j", "k", "keep", "keeps", "kept", "kg",
              "km", "know", "known", "knows", "l", "largely", "last", "lately", "later", "latter", "latterly", "least",
              "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking",
              "looks", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "mean", "means", "meantime",
              "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "moreover", "mostly", "mr", "mrs", "much",
              "mug", "must", "n", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary",
              "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "nobody", "non",
              "none", "nonetheless", "noone", "normally", "nos", "noted", "nothing", "nowhere", "obtain", "obtained",
              "obviously", "often", "oh", "ok", "okay", "old", "omitted", "one", "ones", "onto", "ord", "others",
              "otherwise", "outside", "overall", "owing", "p", "page", "pages", "part", "particular", "particularly",
              "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially",
              "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides",
              "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "readily", "really", "recent",
              "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research",
              "respectively", "resulted", "resulting", "results", "right", "run", "said", "saw", "say", "saying",
              "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves",
              "sent", "seven", "several", "shall", "shed", "shes", "show", "showed", "shown", "showns", "shows",
              "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "somebody", "somehow",
              "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry",
              "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially",
              "successfully", "sufficiently", "suggest", "sup", "sure", "take", "taken", "taking", "tell", "tends",
              "th", "thank", "thanks", "thanx", "thats", "that've", "thence", "thereafter", "thereby", "thered",
              "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've",
              "theyd", "theyre", "think", "thou", "though", "thoughh", "thousand", "throug", "throughout", "thru",
              "thus", "til", "tip", "together", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying",
              "ts", "twice", "two", "u", "un", "unfortunately", "unless", "unlike", "unlikely", "unto", "upon", "ups",
              "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value",
              "various", "'ve", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "wasnt", "way", "wed",
              "welcome", "went", "werent", "whatever", "what'll", "whats", "whence", "whenever", "whereafter",
              "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "whim", "whither", "whod",
              "whoever", "whole", "who'll", "whomever", "whos", "whose", "widely", "willing", "wish", "within",
              "without", "wont", "words", "world", "wouldnt", "www", "x", "yes", "yet", "youd", "youre", "z", "zero",
              "a's", "ain't", "allow", "allows", "apart", "appear", "appreciate", "appropriate", "associated", "best",
              "better", "c'mon", "c's", "cant", "changes", "clearly", "concerning", "consequently", "consider",
              "considering", "corresponding", "course", "currently", "definitely", "described", "despite", "entirely",
              "exactly", "example", "going", "greetings", "hello", "help", "hopefully", "ignored", "inasmuch",
              "indicate", "indicated", "indicates", "inner", "insofar", "it'd", "keep", "keeps", "novel", "presumably",
              "reasonably", "second", "secondly", "sensible", "serious", "seriously", "sure", "t's", "third",
              "thorough", "thoroughly", "three", "well", "wonder", "a", "about", "above", "above", "across", "after",
              "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although",
              "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow",
              "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became",
              "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below",
              "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot",
              "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due",
              "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc",
              "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify",
              "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from",
              "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her",
              "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how",
              "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself",
              "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile",
              "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself",
              "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
              "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto",
              "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per",
              "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems",
              "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
              "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system",
              "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there",
              "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third",
              "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too",
              "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very",
              "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where",
              "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while",
              "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without",
              "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "a", "b", "c", "d", "e", "f",
              "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A",
              "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
              "W", "X", "Y", "Z", "co", "op", "research-articl", "pagecount", "cit", "ibid", "les", "le", "au", "que",
              "est", "pas", "vol", "el", "los", "pp", "u201d", "well-b", "http", "volumtype", "par", "0o", "0s", "3a",
              "3b", "3d", "6b", "6o", "a1", "a2", "a3", "a4", "ab", "ac", "ad", "ae", "af", "ag", "aj", "al", "an",
              "ao", "ap", "ar", "av", "aw", "ax", "ay", "az", "b1", "b2", "b3", "ba", "bc", "bd", "be", "bi", "bj",
              "bk", "bl", "bn", "bp", "br", "bs", "bt", "bu", "bx", "c1", "c2", "c3", "cc", "cd", "ce", "cf", "cg",
              "ch", "ci", "cj", "cl", "cm", "cn", "cp", "cq", "cr", "cs", "ct", "cu", "cv", "cx", "cy", "cz", "d2",
              "da", "dc", "dd", "de", "df", "di", "dj", "dk", "dl", "do", "dp", "dr", "ds", "dt", "du", "dx", "dy",
              "e2", "e3", "ea", "ec", "ed", "ee", "ef", "ei", "ej", "el", "em", "en", "eo", "ep", "eq", "er", "es",
              "et", "eu", "ev", "ex", "ey", "f2", "fa", "fc", "ff", "fi", "fj", "fl", "fn", "fo", "fr", "fs", "ft",
              "fu", "fy", "ga", "ge", "gi", "gj", "gl", "go", "gr", "gs", "gy", "h2", "h3", "hh", "hi", "hj", "ho",
              "hr", "hs", "hu", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ic", "ie", "ig", "ih", "ii",
              "ij", "il", "in", "io", "ip", "iq", "ir", "iv", "ix", "iy", "iz", "jj", "jr", "js", "jt", "ju", "ke",
              "kg", "kj", "km", "ko", "l2", "la", "lb", "lc", "lf", "lj", "ln", "lo", "lr", "ls", "lt", "m2", "ml",
              "mn", "mo", "ms", "mt", "mu", "n2", "nc", "nd", "ne", "ng", "ni", "nj", "nl", "nn", "nr", "ns", "nt",
              "ny", "oa", "ob", "oc", "od", "of", "og", "oi", "oj", "ol", "om", "on", "oo", "oq", "or", "os", "ot",
              "ou", "ow", "ox", "oz", "p1", "p2", "p3", "pc", "pd", "pe", "pf", "ph", "pi", "pj", "pk", "pl", "pm",
              "pn", "po", "pq", "pr", "ps", "pt", "pu", "py", "qj", "qu", "r2", "ra", "rc", "rd", "rf", "rh", "ri",
              "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "rv", "ry", "s2", "sa", "sc", "sd", "se",
              "sf", "si", "sj", "sl", "sm", "sn", "sp", "sq", "sr", "ss", "st", "sy", "sz", "t1", "t2", "t3", "tb",
              "tc", "td", "te", "tf", "th", "ti", "tj", "tl", "tm", "tn", "tp", "tq", "tr", "ts", "tt", "tv", "tx",
              "ue", "ui", "uj", "uk", "um", "un", "uo", "ur", "ut", "va", "wa", "vd", "wi", "vj", "vo", "wo", "vq",
              "vt", "vu", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y2",
              "yj", "yl", "yr", "ys", "yt", "zi", "zz"]

stopn = set([e for e in stop_words])

# Class for creating the neural network.
class Network(tnn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.lstm = torch.nn.LSTM(50, 100, batch_first=True)
        self.conv1 = tnn.Conv1d(50, 50, kernel_size=8, padding=5)
        self.conv2 = tnn.Conv1d(50, 50, kernel_size=8, padding=5)
        self.conv3 = tnn.Conv1d(50, 50, kernel_size=8, padding=5)
        self.fc1 = tnn.Linear(100, 50)
        self.fc2 = tnn.Linear(64, 1)
        self.fc3 = tnn.Linear(50, 1)
        self.dropout = tnn.Dropout(0.5)

    def forward(self, input, length):
        input, (h_n, h_c) = self.lstm(input, None)
        input = tnn.functional.relu(self.fc1(input))

        input = input.permute(0, 2, 1)

        input = self.conv1(input)
        input = tnn.functional.relu(input)
        input = tnn.functional.max_pool1d(input, 4, 4)

        input = self.conv2(input)
        input = tnn.functional.relu(input)
        input = tnn.functional.max_pool1d(input, 4, 4)

        input = self.conv3(input)
        input = tnn.functional.relu(input)

        # input = tnn.functional.max_pool1d(input, input.size(2))
        input = input.max(dim=-1)[0]

        input = input.squeeze()
        input = self.fc3(input)
        return input.flatten()


class PreProcessing():
    def pre(x):
        """Called after tokenization"""
        result = []

        text = " ".join(x)
        text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r",", " ", text)
        text = re.sub(r"\.", " ", text)
        text = re.sub(r"!", " ! ", text)
        text = re.sub(r"\/", " ", text)
        text = re.sub(r"\^", " ^ ", text)
        text = re.sub(r"\+", " + ", text)
        text = re.sub(r"\-", " - ", text)
        text = re.sub(r"\=", " = ", text)
        text = re.sub(r"'", " ", text)
        text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
        text = re.sub(r":", " : ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r" u s ", " american ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r" 9 11 ", "911", text)
        text = re.sub(r"e - mail", "email", text)
        text = re.sub(r"j k", "jk", text)
        text = re.sub(r"\s{2,}", " ", text)
        text = text.split()
        for word in text:
            if word not in stopn and len(word) > 3:
                result.append(word)
        return result

    def post(batch, vocab):
        return batch

    text_field = data.Field(lower=True, include_lengths=True, batch_first=True, preprocessing=pre, postprocessing=post)



file = "glove.6B.50d.txt"


def pre(x):
    """Called after tokenization"""
    result = []

    text = " ".join(x)
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.split()
    for word in text:
        if word not in stopn and len(word) > 2:
            result.append(word)
    return result
import numpy as np

#Loading Glove Model
def loadGloveModel(gloveFile):
    print("Loading Glove Model")

    with open(file, encoding="utf8") as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.", len(model), " words loaded!")
    return model

mo = loadGloveModel(file)

#load textfild
textField = data.Field(lower=True, include_lengths=True, batch_first=True)
with open("TEXT.Field", "rb")as f:
    TEXT = dill.load(f)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("Using device: " + str(device))

#create model
model = Network().to(device)
model.load_state_dict(torch.load('model.pth'))
model.eval()

#predict
def predict_sentiment(sentence):
    tokenized = [tok for tok in sentence.split()]
    tokenized = pre(tokenized)
    indexed = [mo[t.lower()] for t in tokenized if t.lower() in mo.keys()]
    if len(indexed) == 0:
        return 0.5

    tensor = torch.Tensor(indexed).to(device)
    tensor = tensor.unsqueeze(0)

    prediction = torch.sigmoid(model(tensor,1))
    prediction = torch.round(prediction)
    if prediction > 0.5:
        return 1
    else:
        return 0
