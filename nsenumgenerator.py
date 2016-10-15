#!/usr/bin/env python

name = "race waypoint marker shape"
values = [
	"1",
	"2",
	"3",
	"4",
	"5",
	"6"
]
api_value_type = "NSString"
api_value_name = "string"

def title(string):
	modded = string.title()
	modded = modded.replace(" ", "")
	return modded

def title_small_first(string):
	modded = string.title()
	modded = first_lower(modded)
	modded = modded.replace(" ", "")
	return modded

def first_lower(s):
   if len(s) == 0:
      return s
   else:
      return s[0].lower() + s[1:]

def underscore(string):
	return string.replace(" ", "_")

print "-------------- .h ---------------"

# Enum
print """
typedef NS_ENUM(NSUInteger, %(big)s) {
    %(big)sUndefined,""" % {
	"big": title(name)
}

for value in values[:-1]:
	print "    %(big)s%(value_big)s," % {
		"big": title(name),
		"value_big": title(value)
	}
print """    %(big)s%(value_big)s
};""" % {
	"big": title(name),
	"value_big": title(values[-1])
}

# Header declarations
print """
+ (%(big)s)%(small)sFor%(api_value_name_big)s:(%(api_value_type)s *)%(small)s%(api_value_name_big)s;
+ (%(api_value_type)s *)%(api_value_name)sFor%(big)s:(%(big)s)%(small)s;
""" % {
	"big": title(name),
	"small": title_small_first(name),
	"api_value_type": api_value_type,
	"api_value_name_big": title(api_value_name),
	"api_value_name": api_value_name
}

print "-------------- .m ---------------"
# Function name
print """
+ (%(big)s)%(small)sFor%(api_value_name_big)s:(%(api_value_type)s *)%(small)s%(api_value_name_big)s {
    if ([%(small)s%(api_value_name_big)s isEqualTo%(api_value_name_big)s:@"%(value_underscore)s"]) {
        return %(big)s%(value_big)s;""" % {
	"big": title(name),
	"small": title_small_first(name),
	"value_underscore": underscore(values[0]),
	"value_big": title(values[0]),
	"api_value_type": api_value_type,
	"api_value_name_big": title(api_value_name),
	"api_value_name": api_value_name
}
# Else
for value in values[1:]:
	print """    } else if ([%(small)s%(api_value_name_big)s isEqualTo%(api_value_name_big)s:@"%(value_underscore)s"]) {
        return %(big)s%(value_big)s;""" % {
	"big": title(name),
	"small": title_small_first(name),
	"value_underscore": underscore(value),
	"value_big": title(value),
	"api_value_name_big": title(api_value_name),
	}
print "    }"
print """
    return %(big)s%(undefined_big)s;""" % {
	"big": title(name),
	"undefined_big": title("undefined")
	}
print "}"

# Function name
print """
+ (%(api_value_type)s *)%(api_value_name)sFor%(big)s:(%(big)s)%(small)s {
    switch(%(small)s) {""" % {
	"big": title(name),
	"small": title_small_first(name),
	"api_value_type": api_value_type,
	"api_value_name": api_value_name
}
# Values
for value in values:
	print """        case %(big)s%(value_big)s:
            return @"%(value_underscore)s";""" % {
			"big": title(name),
			"value_underscore": underscore(value),
			"value_big": title(value)
         }

print """        default:
            break;
    }

    return nil;
}"""

