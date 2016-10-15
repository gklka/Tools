#!/usr/bin/env python

name = "FDPatientFilePastTreatmentDetailsController"
sections = ["Data", "TreatmentTypes"]
rows = ["Name", "Doctor", "Chair", "StartTime", "EndTime", "TreatmentType", "Price", "Comment"]

section_enum_name = name + "Section"
row_enum_name = name + "Row"

print "--------------- enums -----------------"

# Print enums
print "typedef NS_ENUM(NSUInteger, %s) {" % section_enum_name
print "    %sUndefined," % section_enum_name
for section in sections[:-1]:
	print "    %s%s," % (section_enum_name, section)
print "    %s%s" % (section_enum_name, sections[-1])
print "};\n"

print "typedef NS_ENUM(NSUInteger, %s) {" % row_enum_name
print "    %sUndefined," % row_enum_name
for row in rows[:-1]:
	print "    %s%s," % (row_enum_name, row)
print "    %s%s" % (row_enum_name, rows[-1])
print "};\n"

print "typedef %s SectionType" % section_enum_name
print "typedef %s RowType\n" % row_enum_name

print "--------------- tableview -----------------"

print """
#pragma mark - <UITableViewDataSource>

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return [self sections].count;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return [self rowsForSection:section].count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    RowType rowType = [self rowTypeForIndexPath:indexPath];
    
    switch (rowType) {
""" % {"rowenum": row_enum_name}

for row in rows:
	print """        case %s%s:
	{
	    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"<#Basic Cell#>" forIndexPath:indexPath];
	    return cell;
	}""" % (row_enum_name, row)

print """        default:
            DDLogError(@"ERROR: Missing row type in cellForRowAtIndexPath");
            break;
    }
    
    return nil;
}"""

print "--------------- helper -----------------"

print """#pragma mark - Helper

- (void)setup {
	
}

- (void)refresh {
	[self.tableView reloadData];
}

/**
 Returns the array of sections

 @return Array of `SectionType` enum values wrapped in `NSNumber` objects
 */
- (NSArray *)sections {
    NSMutableArray *sections = [NSMutableArray new];
"""

for section in sections:
	print "        [sections addObject:@(%s%s)];" % (section_enum_name, section)

print """
    return sections;
}

/**
 Get the enum value of the section at a given index

 @param sectionIndex The index to be determined

 @return Enum value
 */
- (SectionType)sectionTypeForSection:(NSUInteger)sectionIndex {
    NSArray *sections = [self sections];
    
    if (sectionIndex < sections.count) {
        NSNumber *type = [sections objectAtIndex:sectionIndex];
        return [type integerValue];
    }
    
    return %(sectiontype)sUndefined;
}

/**
 Returns an array of rows in the given section type

 @param sectionType The section type enum value to get the rows for

 @return Array of `RowType` enum values wrapped in `NSNumber` objects
 */
- (NSArray *)rowsForSectionType:(SectionType)sectionType {
    NSArray *rows = @[];
    
    switch (sectionType) {""" % {
    	"sectiontype": section_enum_name
    }

for section in sections:
	print """        case %s%s:
        {
            rows = @[];
            break;
        }""" % (section_enum_name, section)

print """        default:
            break;
    }
    
    return rows;
}

/**
 Gets the rows for a given section index

 @param sectionIndex The section number to get the rows for

 @return Array of `RowType` enum values wrapped in `NSNumber` objects
 */
- (NSArray *)rowsForSection:(NSUInteger)sectionIndex {
    FDClinicSettingsControllerSection sectionType = [self sectionTypeForSection:sectionIndex];
    return [self rowsForSectionType:sectionType];
}

/**
 Find out the enum type of a row at a given indexpath

 @param indexPath The indexpath of the row to determine the type

 @return Enum value
 */
- (RowType)rowTypeForIndexPath:(NSIndexPath *)indexPath {
    FDClinicSettingsControllerSection sectionType = [self sectionTypeForSection:indexPath.section];
    
    NSArray *rows = [self rowsForSectionType:sectionType];
    
    if (indexPath.row < rows.count) {
        NSNumber *type = [rows objectAtIndex:indexPath.row];
        return [type integerValue];
    }
    
    return FDClinicSettingsControllerRowUndefined;
}

/**
 Returns the indexpath for a given row type in a given section type. Returns `nil`, if the row is not found.

 @param rowType     Row enum type to get the indexpath for
 @param sectionType Section enum type to get the indexpath for

 @return Returns a valid NSIndexPath object or nil
 */
- (NSIndexPath *)indexPathForRow:(RowType)rowType inSection:(SectionType)sectionType {
    NSUInteger sectionIndex = [self sectionNumberForSection:sectionType];
    if (sectionIndex != NSNotFound) {
        NSArray *rows = [self rowsForSection:sectionIndex];
        
        NSUInteger rowIndex = [rows indexOfObject:@(rowType)];
        if (rowIndex != NSNotFound) {
            return [NSIndexPath indexPathForRow:rowIndex inSection:sectionIndex];
        }
    }
    
    return nil;
}

/**
 Get the section index for the given section enum

 @param sectionType The enum value to get the index for

 @return Numeric index for the given enum
 */
- (NSUInteger)sectionNumberForSection:(SectionType)sectionType {
    return [[self sections] indexOfObject:@(sectionType)];
}
""" % {
	"sectiontype": section_enum_name,
	"rowtype": row_enum_name
}
