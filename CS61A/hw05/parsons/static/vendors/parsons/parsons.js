(function($, _) { // wrap in anonymous function to not show some helper variables

   // regexp used for trimming
   var trimRegexp = /^\s*(.*?)\s*$/;
   var givenIndentRegexp = /#(\d+)given\s*/;
   var blankRegexp = /#blank([^#]*)/;
   var userStrings = {
     trash_label: 'Drag from here',
     solution_label: 'Construct your solution here, including indents',
     order: function() {
       return "Code fragments in your program are wrong, or in wrong order. This can be fixed by moving, removing, or replacing highlighted fragments.";},
     lines_missing: function() {
       return "Your program has too few code fragments.";},
     lines_too_many: function() {
       return "Your program has too many code fragments.";},
     no_matching: function(lineNro) {
       return "Based on language syntax, the highlighted fragment (" + lineNro + ") is not correctly indented."; },
     no_matching_open: function(lineNro, block) {
       return "The " + block + " ended on line " + lineNro + " never started."; },
     no_matching_close: function(lineNro, block) {
       return "Block " + block + " defined on line " + lineNro + " not ended properly";
     },
     block_close_mismatch: function(closeLine, closeBlock, openLine, inBlock) {
       return "Cannot end block " + closeBlock + " on line " + closeLine + " when still inside block " + inBlock + " started on line " + openLine;
     },
     block_structure: function(lineNro) { return "The highlighted fragment " + lineNro + " belongs to a wrong block (i.e. indentation)."; },
     unittest_error: function(errormsg) {
       return "<span class='msg'>Error in parsing/executing your program</span><br/> <span class='errormsg'>" + errormsg + "</span>";
     },
     unittest_output_assertion: function(expected, actual) {
      return "Expected output: <span class='expected output'>" + expected + "</span>" +
            "Output of your program: <span class='actual output'>" + actual + "</span>";
     },
     unittest_assertion: function(expected, actual) {
      return "Expected value: <span class='expected'>" + expected + "</span><br>" +
            "Actual value: <span class='actual'>" + actual + "</span>";
     },
     variabletest_assertion: function(varname, expected, actual) {
      return "Expected value of variable " + varname + ": <span class='expected'>" + expected + "</span><br>" +
            "Actual value: <span class='actual'>" + actual + "</span>";
     }
   };

  // Different graders

  var graders = {};
  // The "original" grader for giving line based feedback.
  var LineBasedGrader = function(parson) {
    this.parson = parson;
  };
  graders.LineBasedGrader = LineBasedGrader;
  LineBasedGrader.prototype.grade = function(elementId) {
    var parson = this.parson;
    var elemId = elementId || parson.options.sortableId;
    var student_code = parson.normalizeIndents(parson.getModifiedCode("#ul-" + elemId));
    var lines_to_check = Math.min(student_code.length, parson.model_solution.length);
    var errors = [], log_errors = [];
    var incorrectLines = [], studentCodeLineObjects = [];
    var i;
    var wrong_order = false;

    // Find the line objects for the student's code
    for (i = 0; i < student_code.length; i++) {
      studentCodeLineObjects.push($.extend(true,
                                         {},
                                         parson.getLineById(student_code[i].id)));
    }
    
    // This maps codeline strings to the index, at which starting from 0, we have last
    // found this codeline. This is used to find the best indices for each
    // codeline in the student's code for the LIS computation and, for example,
    // assigns appropriate indices for duplicate lines.
    var lastFoundCodeIndex = {};
    $.each(studentCodeLineObjects, function(index, lineObject) {
      // find the first matching line in the model solution
      // starting from where we have searched previously
      for (var i = (typeof(lastFoundCodeIndex[lineObject.code]) !== 'undefined') ? lastFoundCodeIndex[lineObject.code]+1 : 0;
           i < parson.model_solution.length;
           i++) {
        if (parson.model_solution[i].code === lineObject.code) {
          // found a line in the model solution that matches the student's line
          lastFoundCodeIndex[lineObject.code] = i;
              lineObject.lisIgnore = false;
              // This will be used in LIS computation
            lineObject.position = i;
            break;
        }
      }
      if (i === parson.model_solution.length) {
        if (typeof(lastFoundCodeIndex[lineObject.code]) === 'undefined') {
        // Could not find the line in the model solution at all,
        // it must be a distractor
        // => add to feedback, log, and ignore in LIS computation
          wrong_order = true;
          lineObject.markIncorrectPosition();
        incorrectLines.push(lineObject.orig);
          lineObject.lisIgnore = true;
        } else {
          // The line is part of the solution but there are now
        // too many instances of the same line in the student's code
          // => Let's just have their correct position to be the same
        // as the last one actually found in the solution.
          // LIS computation will handle such duplicates properly and
        // choose only one of the equivalent positions to the LIS and
          // extra duplicates are left in the inverse and highlighted as
        // errors.
          // TODO This method will not always give the most intuitive
        // highlights for lines to supposed to be moved when there are
          // several extra duplicates in the student's code.
            lineObject.lisIgnore = false;
            lineObject.position = lastFoundCodeIndex[lineObject.code];
        }

      }
    });

    var lisStudentCodeLineObjects =
      studentCodeLineObjects.filter(function (lineObject) { return !lineObject.lisIgnore; });
    var inv =
      LIS.best_lise_inverse_indices(lisStudentCodeLineObjects
                      .map(function (lineObject) { return lineObject.position; }));
    $.each(inv, function(_index, lineObjectIndex) {
      // Highlight the lines that could be moved to fix code as defined by the LIS computation
        lisStudentCodeLineObjects[lineObjectIndex].markIncorrectPosition();
        incorrectLines.push(lisStudentCodeLineObjects[lineObjectIndex].orig);
      });
    if (inv.length > 0 || incorrectLines.length > 0) {
      wrong_order = true;
      log_errors.push({type: "incorrectPosition", lines: incorrectLines});
    }

    if (wrong_order) {
      errors.push(parson.translations.order());
    }

    // Check the number of lines in student's code
    if (parson.model_solution.length < student_code.length) {
      $("#ul-" + elemId).addClass("incorrect");
      errors.push(parson.translations.lines_too_many());
      log_errors.push({type: "tooManyLines", lines: student_code.length});
    } else if (parson.model_solution.length > student_code.length){
      $("#ul-" + elemId).addClass("incorrect");
      errors.push(parson.translations.lines_missing());
      log_errors.push({type: "tooFewLines", lines: student_code.length});
    }

    // Finally, check indent if no other errors
    if (errors.length === 0) {
      for (i = 0; i < lines_to_check; i++) {
        var code_line = student_code[i];
        var model_line = parson.model_solution[i];
        if (code_line.indent !== model_line.indent &&
             ((!parson.options.first_error_only) || errors.length === 0)) {
          code_line.markIncorrectIndent();
          errors.push(parson.translations.block_structure(i+1));
          log_errors.push({type: "incorrectIndent", line: (i+1)});
        }
        if (code_line.code == model_line.code &&
             code_line.indent == model_line.indent &&
             errors.length === 0) {
          code_line.markCorrect();
        }
      }
    }

    return {errors: errors, log_errors: log_errors, success: (errors.length === 0)};
  };

  // Create a line object skeleton with only code and indentation from
  // a code string of an assignment definition string (see parseCode)
  var ParsonsCodeline = function(codestring, widget) {
    this.widget = widget;
    this.code = "";
    this.indent = 0;
    if (codestring) {
      // Consecutive lines to be dragged as a single block of code have strings "\\n" to
      // represent newlines => replace them with actual new line characters "\n"
      this.code = codestring.replace(/#distractor\s*$/, "").replace(trimRegexp, "$1").replace(/\\n/g, "\n");
      this.code = codestring.replace(givenIndentRegexp, "").replace(trimRegexp, "$1").replace(/\\n/g, "\n");
      this.indent = codestring.length - codestring.replace(/^\s+/, "").length;
    }
  };
  ParsonsCodeline.prototype.elem = function() {
    // the element will change on shuffle, so we should re-fetch it every time
    return $("#" + this.id);
  };
  ParsonsCodeline.prototype.markCorrect = function() {
    this.elem().addClass(this.widget.FEEDBACK_STYLES.correctPosition);
  };
  ParsonsCodeline.prototype.markIncorrectPosition = function() {
    this.elem().addClass(this.widget.FEEDBACK_STYLES.incorrectPosition);
  };
  ParsonsCodeline.prototype.markIncorrectIndent = function() {
    this.elem().addClass(this.widget.FEEDBACK_STYLES.incorrectIndent);
  };
  // expose the type for testing, extending etc
  window.ParsonsCodeline = ParsonsCodeline;

  // Creates a parsons widget. Init must be called after creating an object.
   var ParsonsWidget = function(options) {
   // Contains line objects of the user-draggable code.
   // The order is not meaningful (unchanged from the initial state) but
   // indent property for each line object is updated as the user moves
   // codelines around. (see parseCode for line object description)
     this.modified_lines = [];
     // contains line objects of distractors (see parseCode for line object description)
     this.extra_lines = [];
     // contains line objects (see parseCode for line object description)
     this.model_solution = [];

     //To collect statistics, feedback should not be based on this
     this.user_actions = [];

     //State history for feedback purposes
     this.state_path = [];
     this.states = {};

     var defaults = {
       'incorrectSound': false,
       'x_indent': 50,
       'can_indent': true,
       'feedback_cb': false,
       'first_error_only': true,
       'max_wrong_lines': 10,
       'lang': 'en',
       'onSortableUpdate': (event, ui) => {}
     };

     this.options = jQuery.extend({}, defaults, options);
     this.feedback_exists = false;
     this.id_prefix = options['sortableId'] + 'codeline';

     // translate trash_label and solution_label
     if (!this.options.hasOwnProperty("trash_label")) {
         this.options.trash_label = userStrings.trash_label;
     }
     if (!this.options.hasOwnProperty("solution_label")) {
         this.options.solution_label = userStrings.solution_label;
     }
     this.FEEDBACK_STYLES = { 'correctPosition' : 'correctPosition',
                              'incorrectPosition' : 'incorrectPosition',
                              'correctIndent' : 'correctIndent',
                              'incorrectIndent' : 'incorrectIndent'};

    // use grader passed as an option if defined and is a function
    if (this.options.grader && _.isFunction(this.options.grader)) {
      this.grader = new this.options.grader(this);
    } else {
      this.grader = new LineBasedGrader(this);
    }
   };
  ParsonsWidget._graders = graders;

   ////Public methods

   // Parses an assignment definition given as a string and returns and
   // transforms this into an object defining the assignment with line objects.
   //
   // lines: A string that defines the solution to the assignment and also
   //   any possible distractors
   // max_distractrors: The number of distractors allowed to be included with
   //   the lines required in the solution
   ParsonsWidget.prototype.parseCode = function(lines, max_distractors) {
     var distractors = [],
         given = [],
         indented = [],
         widgetData = [],
         lineObject,
         errors = [],
         that = this;
     // Create line objects out of each codeline and separate
     // lines belonging to the solution and distractor lines
     // Fields in line objects:
     //   code: a string of the code, may include newline characters and
     //     thus in fact represents a block of consecutive lines
     //   indent: indentation level, -1 for distractors
     //   distractor: boolean whether this is a distractor
     //   orig: the original index of the line in the assignment definition string,
     //     for distractors this is not meaningful but for lines belonging to the
     //     solution, this is their expected position
     $.each(lines, function(index, item) {
       lineObject = new ParsonsCodeline(item, that);
       lineObject.orig = index;
        if (item.search(/#distractor\s*$/) >= 0) {
          // This line is a distractor
          lineObject.indent = -1;
          lineObject.distractor = true;
          if (lineObject.code.length > 0) {
            // The line is non-empty, not just whitespace
            distractors.push(lineObject);
          }
        // These lines are part of the final solution
        } else if (item.search(givenIndentRegexp) >= 0) {
          if (lineObject.code.length > 0) {
            lineObject.indent = parseInt(item.match(givenIndentRegexp)[1]);
            lineObject.distractor = false;
            given.push(lineObject)
          }
        } else {
          // Initialize line object with code and indentation properties
          if (lineObject.code.length > 0) {
            // The line is non-empty, not just whitespace
            lineObject.distractor = false;
            indented.push(lineObject);
          }
        }
     });

     var normalized = this.normalizeIndents(indented);

     $.each(normalized, function(index, item) {
              if (item.indent < 0) {
                // Indentation error
                errors.push(userStrings.no_matching(normalized.orig));
              }
              widgetData.push(item);
            });

     $.each(given, function(index, item) {
        widgetData.push(item);
      });

     // Remove extra distractors if there are more alternative distrators
     // than should be shown at a time
     var permutation = this.getRandomPermutation(distractors.length);
     var selected_distractors = [];
     for (var i = 0; i < max_distractors; i++) {
       selected_distractors.push(distractors[permutation[i]]);
       widgetData.push(distractors[permutation[i]]);
     }

     return {
       // an array of line objects specifying  the solution
       solution:  $.extend(true, [], normalized),
       // an array of line objects specifying the requested number
       // of distractors (not all possible alternatives)
       distractors: $.extend(true, [], selected_distractors),
       given: $.extend(true, [], given),
       // an array of line objects specifying the initial code arrangement
       // given to the user to use in constructing the solution
       widgetInitial: $.extend(true, [], widgetData),
       errors: errors};
   };

   ParsonsWidget.prototype.init = function(text) {
     // TODO: Error handling, parseCode may return errors in an array in property named errors.
     var initial_structures = this.parseCode(text.split("\n"), this.options.max_wrong_lines);
     this.model_solution = initial_structures.solution;
     this.given = initial_structures.given;
     this.extra_lines = initial_structures.distractors;
     this.modified_lines = initial_structures.widgetInitial;
     var id_prefix = this.id_prefix;

     // Add ids to the line objects in the user-draggable lines
     $.each(this.modified_lines, function(index, item) {
       item.id = id_prefix + index;
       // item.indent = 0;
     });
   };

   ParsonsWidget.prototype.getHash = function(searchString) {
     var hash = [],
         ids = $(searchString).sortable('toArray'),
         line;
     for (var i = 0; i < ids.length; i++) {
       line = this.getLineById(ids[i]);
       hash.push(line.orig + "_" + line.indent);
     }
     //prefix with something to handle empty output situations
     if (hash.length === 0) {
       return "-";
     } else {
       return hash.join("-");
     }
   };

   ParsonsWidget.prototype.solutionHash = function() {
       return this.getHash("#ul-" + this.options.sortableId);
   };

   ParsonsWidget.prototype.trashHash = function() {
       return this.getHash("#ul-" + this.options.trashId);
   };

   ParsonsWidget.prototype.solutionCode = function() {
     var indentConstant = "    ";
     // var indentConstant = "  ";
     var solutionCode = "";
     var codeMetadata = "";
     var lines = this.normalizeIndents(this.getModifiedCode("#ul-" + this.options.sortableId));
     for (let i = 0; i < lines.length; i++) {
       var blankText = "";
       //Original line from the YAML File
       var originalLine = "";
       let yamlConfigClone = $("#" + lines[i].id).clone();
       yamlConfigClone.find("input").each(function (_, inp) {
           inp.replaceWith('!BLANK');
           blankText += " #blank" + inp.value
       });
       let codeClone = $("#" + lines[i].id).clone();
       codeClone.find("input").each(function (_, inp) {
           inp.replaceWith(inp.value);
       });
       yamlConfigClone[0].innerText = yamlConfigClone[0].innerText.trimRight();
       codeClone[0].innerText = codeClone[0].innerText.trimRight();
       if (yamlConfigClone[0].innerText != codeClone[0].innerText) {
         originalLine = " #!ORIGINAL" + yamlConfigClone[0].innerText + blankText;
       }
       solutionCode += indentConstant.repeat(lines[i].indent) + codeClone[0].innerText + "\n";
       codeMetadata +=  originalLine + "\n";
     }
     return [solutionCode, codeMetadata];
   };
   
   	
   ParsonsWidget.prototype.parsonsReprCode = function() {	
    var solutionCode = "";	
    var reprCodeSoln = "";	
    var reprCodeNonSoln = "";	
    var lines = this.normalizeIndents(this.getModifiedCode("#ul-" + this.options.sortableId));	
    var lines_in_soln = [];	
    // find lines in solution	
    for (let i = 0; i < lines.length; i++) {	
      lines_in_soln.push(lines[i].id);	
      var blankText = "";	
      let yamlConfigClone = $("#" + lines[i].id).clone();	
      yamlConfigClone.find("input").each(function (_, inp) {	
          inp.replaceWith('!BLANK');	
          blankText += " #blank" + inp.value	
      });	
      let codeClone = $("#" + lines[i].id).clone();	
      codeClone.find("input").each(function (_, inp) {	
          inp.replaceWith(inp.value);	
      });	
      yamlConfigClone[0].innerText = yamlConfigClone[0].innerText.trimRight();	
      codeClone[0].innerText = codeClone[0].innerText.trimRight();	
      	
      // remove line numbers at the end of each line	
      // is not a problem in solutionCode(), worth investigating	
      var line = yamlConfigClone[0].innerText;	
      var tokensLst = line.split(" ");	
      tokensLst.pop(); 	
      line = tokensLst.join(" ");	
      line = line + ` #${lines[i].indent}given` + blankText;	
      reprCodeSoln +=  line + "\n";	
    }	
    for (let i = 0; i < this.modified_lines.length; i++) {	
      if (!lines_in_soln.includes(this.modified_lines[i].id)) {	
        var blankText = "";	
        let yamlConfigClone = $("#" + this.modified_lines[i].id).clone();	
        yamlConfigClone.find("input").each(function (_, inp) {	
            inp.replaceWith('!BLANK');	
            blankText += " #blank" + inp.value	
        });	
        let codeClone = $("#" + this.modified_lines[i].id).clone();	
        codeClone.find("input").each(function (_, inp) {	
            inp.replaceWith(inp.value);	
        });	
        yamlConfigClone[0].innerText = yamlConfigClone[0].innerText.trimRight();	
        codeClone[0].innerText = codeClone[0].innerText.trimRight();	
        var line = yamlConfigClone[0].innerText;	
        reprCodeNonSoln += line + "\n";	
      }	
    }	
    return reprCodeSoln + reprCodeNonSoln;	
   };

   ParsonsWidget.prototype.addLogEntry = function(entry) {
     var state, previousState;
     var logData = {
       time: new Date(),
       output: this.solutionHash(),
       type: "action"
     };

     if (this.options.trashId) {
       logData.input = this.trashHash();
     }

     if (entry.target) {
       entry.target = entry.target.replace(this.id_prefix, "");
     }

     state = logData.output;

     jQuery.extend(logData, entry);
     this.user_actions.push(logData);

     //Updating the state history
     if(this.state_path.length > 0) {
       previousState = this.state_path[this.state_path.length - 1];
       this.states[previousState] = logData;
     }

     //Add new item to the state path only if new and previous states are not equal
     if (this.state_path[this.state_path.length - 1] !== state) {
       this.state_path.push(state);
     }
     // callback for reacting to actions
     if ($.isFunction(this.options.action_cb)) {
       this.options.action_cb.call(this, logData);
     }
   };

   /**
    * Update indentation of a line based on new coordinates
    * leftDiff horizontal difference from (before and after drag) in px
    ***/
   ParsonsWidget.prototype.updateIndent = function(leftDiff, id) {

     var code_line = this.getLineById(id);
     var new_indent = this.options.can_indent ? code_line.indent + Math.floor(leftDiff / this.options.x_indent) : 0;
     new_indent = Math.max(0, new_indent);
     code_line.indent = new_indent;

     return new_indent;
   };

   // Get a line object by the full id including id prefix
   // (see parseCode for description of line objects)
   ParsonsWidget.prototype.getLineById = function(id) {
     var index = -1;
     for (var i = 0; i < this.modified_lines.length; i++) {
       if (this.modified_lines[i].id == id) {
         index = i;
         break;
       }
     }
     return this.modified_lines[index];
   };

   // Check and normalize code indentation.
   // Does not use the current object (this) ro make changes to
   // the parameter.
   // Returns a new array of line objects whose indent fields' values
   // may be different from the argument. If indentation does not match,
   // i.e. code is malformed, value of indent may be -1.
   // For example, the first line may not be indented.
   ParsonsWidget.prototype.normalizeIndents = function(lines) {
     // Our code doesn't require indents to be normalized. However, this code
     // breaks when a line has an unindent that does not match outer indentation
     // level.
     return lines;

     var normalized = [];
     var new_line;
     var match_indent = function(index) {
       //return line index from the previous lines with matching indentation
       for (var i = index-1; i >= 0; i--) {
         if (lines[i].indent == lines[index].indent) {
           return normalized[i].indent;
         }
       }
       return -1;
     };
     for ( var i = 0; i < lines.length; i++ ) {
       //create shallow copy from the line object
       new_line = jQuery.extend({}, lines[i]);
       if (i === 0) {
         new_line.indent = 0;
         if (lines[i].indent !== 0) {
           new_line.indent = -1;
         }
       } else if (lines[i].indent == lines[i-1].indent) {
         new_line.indent = normalized[i-1].indent;
       } else if (lines[i].indent > lines[i-1].indent) {
         new_line.indent = normalized[i-1].indent + 1;
       } else {
         // indentation can be -1 if no matching indentation exists, i.e. IndentationError in Python
         new_line.indent = match_indent(i);
       }
       normalized[i] = new_line;
     }
     return normalized;
   };

   /**
    * Retrieve the code lines based on what is in the DOM
    *
    * TODO(petri) refactor to UI
    * */
   ParsonsWidget.prototype.getModifiedCode = function(search_string) {
     //ids of the the modified code
     var lines_to_return = [],
          solution_ids = $(search_string).sortable('toArray'),
          i, item;
     for (i = 0; i < solution_ids.length; i++) {
       item = this.getLineById(solution_ids[i]);
       lines_to_return.push($.extend(new ParsonsCodeline(), item));
     }
     return lines_to_return;
   };

   ParsonsWidget.prototype.hashToIDList = function(hash) {
     var lines = [];
     var lineValues;
     var lineObject;
     var h;

     if (hash === "-" || hash === "" || hash === null) {
       h = [];
     } else {
       h = hash.split("-");
     }

     var ids = [];
     for (var i = 0; i < h.length; i++) {
       lineValues = h[i].split("_");
       ids.push(this.modified_lines[lineValues[0]].id);
     }
     return ids;
   };

   ParsonsWidget.prototype.updateIndentsFromHash = function(hash) {
     var lineValues;
     var h;

     if (hash === "-" || hash === "" || hash === null) {
       h = [];
     } else {
       h = hash.split("-");
     }

     var ids = [];
     for (var i = 0; i < h.length; i++) {
         lineValues = h[i].split("_");
         this.modified_lines[lineValues[0]].indent = Number(lineValues[1]);
         this.updateHTMLIndent(this.modified_lines[lineValues[0]].id);
     }
     return ids;
   };


   /**
    * TODO(petri) refoctor to UI
    */
   ParsonsWidget.prototype.displayError = function(message) {
     if (this.options.incorrectSound && $.sound) {
       $.sound.play(this.options.incorrectSound);
     }
     alert(message);
   };

   ParsonsWidget.prototype.colorFeedback = function(elemId) {
     return new LineBasedGrader(this).grade(elemId);
   };




   /**
    * @return
    * TODO(petri): Separate UI from here
    */
   ParsonsWidget.prototype.getFeedback = function() {
     this.feedback_exists = true;
     var fb = this.grader.grade();
     if (this.options.feedback_cb) {
       this.options.feedback_cb(fb); //TODO(petri): what is needed?
     }
     // if answer is correct, mark it in the UI
     if (fb.success) {
       $("#ul-" + this.options.sortableId).addClass("correct");
     }
     // log the feedback and return; based on the type of grader
     if ('html' in fb) { // unittest/vartests type feedback
       this.addLogEntry({type: "feedback", tests: fb.tests, success: fb.success});
       return { feedback: fb.html, success: fb.success };
     } else {
       this.addLogEntry({type: "feedback", errors: fb.log_errors, success: fb.success});
       return fb.errors;
     }
   };

   ParsonsWidget.prototype.clearFeedback = function() {
     if (this.feedback_exists) {
       $("#ul-" + this.options.sortableId).removeClass("incorrect correct");
       var li_elements = $("#ul-" + this.options.sortableId + " li");
       $.each(this.FEEDBACK_STYLES, function(index, value) {
                li_elements.removeClass(value);
              });
     }
     this.feedback_exists = false;
   };


   ParsonsWidget.prototype.getRandomPermutation = function(n) {
     var permutation = [];
     var i;
     for (i = 0; i < n; i++) {
       permutation.push(i);
     }
     var swap1, swap2, tmp;
     for (i = 0; i < n; i++) {
       swap1 = Math.floor(Math.random() * n);
       swap2 = Math.floor(Math.random() * n);
       tmp = permutation[swap1];
       permutation[swap1] = permutation[swap2];
       permutation[swap2] = tmp;
     }
     return permutation;
   };


   ParsonsWidget.prototype.shuffleLines = function() {
       var permutation = (this.options.permutation?this.options.permutation:this.getRandomPermutation)(this.modified_lines.length);
       var idlist = [];
       for(var i in permutation) {
           idlist.push(this.modified_lines[permutation[i]].id);
       }
       if (this.options.trashId) {
           this.createHTMLFromLists([],idlist);
       } else {
           this.createHTMLFromLists(idlist,[]);
       }
   };

   ParsonsWidget.prototype.alphabetize = function() {
       function compare(a, b) {
           // TODO(nweinman): Remove these conditionals once new print/comment UI is ready.
           if (a.code.startsWith('#')) {
             return 1;
           } else if (a.code.startsWith('print(')) {
             return 1;
           } else if (a.code.startsWith('p !BLANK')) {
             return 1;
           } else if (b.code.startsWith('#')) {
             return -1;
           } else if (b.code.startsWith('print(')) {
             return -1;
           } else if (b.code.startsWith('p !BLANK')) {
             return -1;
           } else if (a.code > b.code) {
               return 1;
           } else if (a.code < b.code) {
               return -1;
           } else {
               return 0;
           }
       }
       var codeLines = this.modified_lines.slice();
       codeLines.sort(compare);
       var idlist = [];
       for (i = 0; i < codeLines.length; i += 1) {
           if (this.given.slice().indexOf(codeLines[i]) < 0) {
             idlist.push(codeLines[i].id);
           }
       }
       var givenCodeLines = this.given.slice();
       var givenIdlist = [];
       for (i = 0; i < givenCodeLines.length; i += 1) {
           givenIdlist.push(givenCodeLines[i].id);
       }
       if (this.options.trashId) {
           this.createHTMLFromLists(givenIdlist,idlist);
       } else {
           this.createHTMLFromLists(idlist,[]);
       }

       // TODO: Move somewhere else or remove after better UI PR.
       codeLines.forEach(function(codeLine) {
         if (codeLine.code.startsWith('# <input') || codeLine.code.includes('DEBUG') || codeLine.code.startsWith('p <input')) {
           $('#' + codeLine.id).css('background-color', 'lightblue');
         }
       });
   };

   ParsonsWidget.prototype.createHTMLFromHashes = function(solutionHash, trashHash) {
       var solution = this.hashToIDList(solutionHash);
       var trash = this.hashToIDList(trashHash);
       this.createHTMLFromLists(solution, trash);
       this.updateIndentsFromHash(solutionHash);
   };

    ParsonsWidget.prototype.updateHTMLIndent = function(codelineID) {
        var line = this.getLineById(codelineID);
        $('#' + codelineID).css("margin-left", this.options.x_indent * line.indent + "px");
        this.updateVertLines();
    };

    ParsonsWidget.prototype.updateVertLines = function(excludedItem) {
      if (!this.options.can_indent) {
        return;
      }

      var maxIndent = 0;
      this.modified_lines.forEach(function (line) {
        if (!excludedItem || line != excludedItem) {
          maxIndent = Math.max(maxIndent, line.indent);
        }
      });
      // Get current indents
      var element = $('#ul-' + this.options.sortableId);
      var backgroundColor = element.css('background-color')
      var backgroundPosition = '';
      for (var i = 1; i <= maxIndent + 1; i++ ) {
        backgroundPosition += i*this.options.x_indent + 'px 0, ';
      }
      element.css({
        'background': 'linear-gradient(#ee0, #ee0) no-repeat border-box, '.repeat(maxIndent).slice(0) +
        'repeating-linear-gradient(0,#ee0,#ee0 10px,'+backgroundColor+' 10px, ' + backgroundColor + ' 20px) no-repeat border-box',
        'background-size': '1px 100%, '.repeat(maxIndent + 1).slice(0, -2),
        'background-position': backgroundPosition.slice(0, -2),
        'background-origin': 'padding-box, '.repeat(maxIndent + 1).slice(0, -2),
        'background-color': backgroundColor,
      });
    }

    ParsonsWidget.prototype.codeLineToHTML = function(codeline) {
      while (codeline.code.search(/!BLANK/) >= 0) {
        var replaceText = "";
        if (codeline.code.search(blankRegexp) >= 0) {
          replaceText = codeline.code.match(blankRegexp)[1].trim().replace(/\"/g, "&quot;").replace(/\'/g, "&apos;");          codeline.code = codeline.code.replace(blankRegexp, "");
        }
        codeline.code = codeline.code.replace(/!BLANK/, function() {
          return "<input type='text' class='text-box' value=\"" + replaceText + "\" " +
              "style = 'width: " + ((replaceText.length + 3) * 8) + 'px\'' +
              "onkeypress=\"this.style.width = ((this.value.length + 3) * 8) + 'px';\"'/>"
        });
      }
      return '<li id="' + codeline.id + '" class="prettyprint ' + this.options['syntax_language'] + ' ">' + codeline.code + '<\/li>';
    };

    ParsonsWidget.prototype.codeLinesToHTML = function(codelineIDs, destinationID) {
        var lineHTML = [];
        for(var id in codelineIDs) {
            var line = this.getLineById(codelineIDs[id]);
            lineHTML.push(this.codeLineToHTML(line));
        }
        return '<ul id="ul-' + destinationID + '">'+lineHTML.join('')+'</ul>';
    };

   /** modifies the DOM by inserting exercise elements into it */
   ParsonsWidget.prototype.createHTMLFromLists = function(solutionIDs, trashIDs) {
     var html;
     if (this.options.trashId) {
       html = (this.options.trash_label?'<p>'+this.options.trash_label+'</p>':'') +
         this.codeLinesToHTML(trashIDs, this.options.trashId);
       $("#" + this.options.trashId).html(html);
       html = (this.options.solution_label?'<p>'+this.options.solution_label+'</p>':'') +
         this.codeLinesToHTML(solutionIDs, this.options.sortableId);
       $("#" + this.options.sortableId).html(html);
     } else {
       html = this.codeLinesToHTML(solutionIDs, this.options.sortableId);
       $("#" + this.options.sortableId).html(html);
     }

     if (window.prettyPrint && (typeof(this.options.prettyPrint) === "undefined" || this.options.prettyPrint)) {
       prettyPrint();
     }

     var that = this;
     var sortable = $("#ul-" + this.options.sortableId).sortable(
       {
         start : function() { that.clearFeedback(); },
         stop : function(event, ui) {
           if ($(event.target)[0] != ui.item.parent()[0]) {
             return;
           }
           that.updateIndent(ui.position.left - ui.item.parent().position().left,
                                       ui.item[0].id);
           that.updateHTMLIndent(ui.item[0].id);
           that.addLogEntry({type: "moveOutput", target: ui.item[0].id}, true);
         },
         receive : function(event, ui) {
           var ind = that.updateIndent(ui.position.left - ui.item.parent().position().left,
                                       ui.item[0].id);
           that.updateHTMLIndent(ui.item[0].id);
           that.addLogEntry({type: "addOutput", target: ui.item[0].id}, true);
         },
         update: that.options.onSortableUpdate,
         grid : that.options.can_indent ? [that.options.x_indent, 1 ] : false
       });
     sortable.addClass("output");
     if (this.options.trashId) {
       var trash = $("#ul-" + this.options.trashId).sortable(
         {
           connectWith: sortable,
           start: function() { that.clearFeedback(); },
           receive: function(event, ui) {
             that.getLineById(ui.item[0].id).indent = 0;
             that.updateHTMLIndent(ui.item[0].id);
             that.addLogEntry({type: "removeOutput", target: ui.item[0].id}, true);
           },
           stop: function(event, ui) {
             if ($(event.target)[0] != ui.item.parent()[0]) {
               // line moved to output and logged there
               return;
             }
             that.addLogEntry({type: "moveInput", target: ui.item[0].id}, true);
           }
         });
       sortable.sortable('option', 'connectWith', trash);
     }
     $.each(solutionIDs, function(index, id) {
       that.updateHTMLIndent(id);
     })
     // Log the original codelines in the exercise in order to be able to
     // match the input/output hashes to the code later on. We need only a
     // few properties of the codeline objects
     var bindings = [];
     for (var i = 0; i < this.modified_lines.length; i++) {
       var line = this.modified_lines[i];
       bindings.push({code: line.code, distractor: line.distractor})
     }
     this.addLogEntry({type: 'init', time: new Date(), bindings: bindings});
   };


   window['ParsonsWidget'] = ParsonsWidget;
 }
// allows _ and $ to be modified with noconflict without changing the globals
// that parsons uses
)($,_);
