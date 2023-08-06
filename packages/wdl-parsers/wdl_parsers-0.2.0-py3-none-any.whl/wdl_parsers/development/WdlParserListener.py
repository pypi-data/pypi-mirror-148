# Generated from WdlParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .WdlParser import WdlParser
else:
    from WdlParser import WdlParser

# This class defines a complete listener for a parse tree produced by WdlParser.
class WdlParserListener(ParseTreeListener):

    # Enter a parse tree produced by WdlParser#map_type.
    def enterMap_type(self, ctx:WdlParser.Map_typeContext):
        pass

    # Exit a parse tree produced by WdlParser#map_type.
    def exitMap_type(self, ctx:WdlParser.Map_typeContext):
        pass


    # Enter a parse tree produced by WdlParser#array_type.
    def enterArray_type(self, ctx:WdlParser.Array_typeContext):
        pass

    # Exit a parse tree produced by WdlParser#array_type.
    def exitArray_type(self, ctx:WdlParser.Array_typeContext):
        pass


    # Enter a parse tree produced by WdlParser#pair_type.
    def enterPair_type(self, ctx:WdlParser.Pair_typeContext):
        pass

    # Exit a parse tree produced by WdlParser#pair_type.
    def exitPair_type(self, ctx:WdlParser.Pair_typeContext):
        pass


    # Enter a parse tree produced by WdlParser#type_base.
    def enterType_base(self, ctx:WdlParser.Type_baseContext):
        pass

    # Exit a parse tree produced by WdlParser#type_base.
    def exitType_base(self, ctx:WdlParser.Type_baseContext):
        pass


    # Enter a parse tree produced by WdlParser#wdl_type.
    def enterWdl_type(self, ctx:WdlParser.Wdl_typeContext):
        pass

    # Exit a parse tree produced by WdlParser#wdl_type.
    def exitWdl_type(self, ctx:WdlParser.Wdl_typeContext):
        pass


    # Enter a parse tree produced by WdlParser#unbound_decls.
    def enterUnbound_decls(self, ctx:WdlParser.Unbound_declsContext):
        pass

    # Exit a parse tree produced by WdlParser#unbound_decls.
    def exitUnbound_decls(self, ctx:WdlParser.Unbound_declsContext):
        pass


    # Enter a parse tree produced by WdlParser#bound_decls.
    def enterBound_decls(self, ctx:WdlParser.Bound_declsContext):
        pass

    # Exit a parse tree produced by WdlParser#bound_decls.
    def exitBound_decls(self, ctx:WdlParser.Bound_declsContext):
        pass


    # Enter a parse tree produced by WdlParser#any_decls.
    def enterAny_decls(self, ctx:WdlParser.Any_declsContext):
        pass

    # Exit a parse tree produced by WdlParser#any_decls.
    def exitAny_decls(self, ctx:WdlParser.Any_declsContext):
        pass


    # Enter a parse tree produced by WdlParser#number.
    def enterNumber(self, ctx:WdlParser.NumberContext):
        pass

    # Exit a parse tree produced by WdlParser#number.
    def exitNumber(self, ctx:WdlParser.NumberContext):
        pass


    # Enter a parse tree produced by WdlParser#string_part.
    def enterString_part(self, ctx:WdlParser.String_partContext):
        pass

    # Exit a parse tree produced by WdlParser#string_part.
    def exitString_part(self, ctx:WdlParser.String_partContext):
        pass


    # Enter a parse tree produced by WdlParser#string_expr_part.
    def enterString_expr_part(self, ctx:WdlParser.String_expr_partContext):
        pass

    # Exit a parse tree produced by WdlParser#string_expr_part.
    def exitString_expr_part(self, ctx:WdlParser.String_expr_partContext):
        pass


    # Enter a parse tree produced by WdlParser#string_expr_with_string_part.
    def enterString_expr_with_string_part(self, ctx:WdlParser.String_expr_with_string_partContext):
        pass

    # Exit a parse tree produced by WdlParser#string_expr_with_string_part.
    def exitString_expr_with_string_part(self, ctx:WdlParser.String_expr_with_string_partContext):
        pass


    # Enter a parse tree produced by WdlParser#string.
    def enterString(self, ctx:WdlParser.StringContext):
        pass

    # Exit a parse tree produced by WdlParser#string.
    def exitString(self, ctx:WdlParser.StringContext):
        pass


    # Enter a parse tree produced by WdlParser#primitive_literal.
    def enterPrimitive_literal(self, ctx:WdlParser.Primitive_literalContext):
        pass

    # Exit a parse tree produced by WdlParser#primitive_literal.
    def exitPrimitive_literal(self, ctx:WdlParser.Primitive_literalContext):
        pass


    # Enter a parse tree produced by WdlParser#expr.
    def enterExpr(self, ctx:WdlParser.ExprContext):
        pass

    # Exit a parse tree produced by WdlParser#expr.
    def exitExpr(self, ctx:WdlParser.ExprContext):
        pass


    # Enter a parse tree produced by WdlParser#infix0.
    def enterInfix0(self, ctx:WdlParser.Infix0Context):
        pass

    # Exit a parse tree produced by WdlParser#infix0.
    def exitInfix0(self, ctx:WdlParser.Infix0Context):
        pass


    # Enter a parse tree produced by WdlParser#infix1.
    def enterInfix1(self, ctx:WdlParser.Infix1Context):
        pass

    # Exit a parse tree produced by WdlParser#infix1.
    def exitInfix1(self, ctx:WdlParser.Infix1Context):
        pass


    # Enter a parse tree produced by WdlParser#lor.
    def enterLor(self, ctx:WdlParser.LorContext):
        pass

    # Exit a parse tree produced by WdlParser#lor.
    def exitLor(self, ctx:WdlParser.LorContext):
        pass


    # Enter a parse tree produced by WdlParser#infix2.
    def enterInfix2(self, ctx:WdlParser.Infix2Context):
        pass

    # Exit a parse tree produced by WdlParser#infix2.
    def exitInfix2(self, ctx:WdlParser.Infix2Context):
        pass


    # Enter a parse tree produced by WdlParser#land.
    def enterLand(self, ctx:WdlParser.LandContext):
        pass

    # Exit a parse tree produced by WdlParser#land.
    def exitLand(self, ctx:WdlParser.LandContext):
        pass


    # Enter a parse tree produced by WdlParser#eqeq.
    def enterEqeq(self, ctx:WdlParser.EqeqContext):
        pass

    # Exit a parse tree produced by WdlParser#eqeq.
    def exitEqeq(self, ctx:WdlParser.EqeqContext):
        pass


    # Enter a parse tree produced by WdlParser#lt.
    def enterLt(self, ctx:WdlParser.LtContext):
        pass

    # Exit a parse tree produced by WdlParser#lt.
    def exitLt(self, ctx:WdlParser.LtContext):
        pass


    # Enter a parse tree produced by WdlParser#infix3.
    def enterInfix3(self, ctx:WdlParser.Infix3Context):
        pass

    # Exit a parse tree produced by WdlParser#infix3.
    def exitInfix3(self, ctx:WdlParser.Infix3Context):
        pass


    # Enter a parse tree produced by WdlParser#gte.
    def enterGte(self, ctx:WdlParser.GteContext):
        pass

    # Exit a parse tree produced by WdlParser#gte.
    def exitGte(self, ctx:WdlParser.GteContext):
        pass


    # Enter a parse tree produced by WdlParser#neq.
    def enterNeq(self, ctx:WdlParser.NeqContext):
        pass

    # Exit a parse tree produced by WdlParser#neq.
    def exitNeq(self, ctx:WdlParser.NeqContext):
        pass


    # Enter a parse tree produced by WdlParser#lte.
    def enterLte(self, ctx:WdlParser.LteContext):
        pass

    # Exit a parse tree produced by WdlParser#lte.
    def exitLte(self, ctx:WdlParser.LteContext):
        pass


    # Enter a parse tree produced by WdlParser#gt.
    def enterGt(self, ctx:WdlParser.GtContext):
        pass

    # Exit a parse tree produced by WdlParser#gt.
    def exitGt(self, ctx:WdlParser.GtContext):
        pass


    # Enter a parse tree produced by WdlParser#add.
    def enterAdd(self, ctx:WdlParser.AddContext):
        pass

    # Exit a parse tree produced by WdlParser#add.
    def exitAdd(self, ctx:WdlParser.AddContext):
        pass


    # Enter a parse tree produced by WdlParser#sub.
    def enterSub(self, ctx:WdlParser.SubContext):
        pass

    # Exit a parse tree produced by WdlParser#sub.
    def exitSub(self, ctx:WdlParser.SubContext):
        pass


    # Enter a parse tree produced by WdlParser#infix4.
    def enterInfix4(self, ctx:WdlParser.Infix4Context):
        pass

    # Exit a parse tree produced by WdlParser#infix4.
    def exitInfix4(self, ctx:WdlParser.Infix4Context):
        pass


    # Enter a parse tree produced by WdlParser#mod.
    def enterMod(self, ctx:WdlParser.ModContext):
        pass

    # Exit a parse tree produced by WdlParser#mod.
    def exitMod(self, ctx:WdlParser.ModContext):
        pass


    # Enter a parse tree produced by WdlParser#mul.
    def enterMul(self, ctx:WdlParser.MulContext):
        pass

    # Exit a parse tree produced by WdlParser#mul.
    def exitMul(self, ctx:WdlParser.MulContext):
        pass


    # Enter a parse tree produced by WdlParser#divide.
    def enterDivide(self, ctx:WdlParser.DivideContext):
        pass

    # Exit a parse tree produced by WdlParser#divide.
    def exitDivide(self, ctx:WdlParser.DivideContext):
        pass


    # Enter a parse tree produced by WdlParser#infix5.
    def enterInfix5(self, ctx:WdlParser.Infix5Context):
        pass

    # Exit a parse tree produced by WdlParser#infix5.
    def exitInfix5(self, ctx:WdlParser.Infix5Context):
        pass


    # Enter a parse tree produced by WdlParser#expr_infix5.
    def enterExpr_infix5(self, ctx:WdlParser.Expr_infix5Context):
        pass

    # Exit a parse tree produced by WdlParser#expr_infix5.
    def exitExpr_infix5(self, ctx:WdlParser.Expr_infix5Context):
        pass


    # Enter a parse tree produced by WdlParser#pair_literal.
    def enterPair_literal(self, ctx:WdlParser.Pair_literalContext):
        pass

    # Exit a parse tree produced by WdlParser#pair_literal.
    def exitPair_literal(self, ctx:WdlParser.Pair_literalContext):
        pass


    # Enter a parse tree produced by WdlParser#apply.
    def enterApply(self, ctx:WdlParser.ApplyContext):
        pass

    # Exit a parse tree produced by WdlParser#apply.
    def exitApply(self, ctx:WdlParser.ApplyContext):
        pass


    # Enter a parse tree produced by WdlParser#expression_group.
    def enterExpression_group(self, ctx:WdlParser.Expression_groupContext):
        pass

    # Exit a parse tree produced by WdlParser#expression_group.
    def exitExpression_group(self, ctx:WdlParser.Expression_groupContext):
        pass


    # Enter a parse tree produced by WdlParser#primitives.
    def enterPrimitives(self, ctx:WdlParser.PrimitivesContext):
        pass

    # Exit a parse tree produced by WdlParser#primitives.
    def exitPrimitives(self, ctx:WdlParser.PrimitivesContext):
        pass


    # Enter a parse tree produced by WdlParser#left_name.
    def enterLeft_name(self, ctx:WdlParser.Left_nameContext):
        pass

    # Exit a parse tree produced by WdlParser#left_name.
    def exitLeft_name(self, ctx:WdlParser.Left_nameContext):
        pass


    # Enter a parse tree produced by WdlParser#at.
    def enterAt(self, ctx:WdlParser.AtContext):
        pass

    # Exit a parse tree produced by WdlParser#at.
    def exitAt(self, ctx:WdlParser.AtContext):
        pass


    # Enter a parse tree produced by WdlParser#negate.
    def enterNegate(self, ctx:WdlParser.NegateContext):
        pass

    # Exit a parse tree produced by WdlParser#negate.
    def exitNegate(self, ctx:WdlParser.NegateContext):
        pass


    # Enter a parse tree produced by WdlParser#unirarysigned.
    def enterUnirarysigned(self, ctx:WdlParser.UnirarysignedContext):
        pass

    # Exit a parse tree produced by WdlParser#unirarysigned.
    def exitUnirarysigned(self, ctx:WdlParser.UnirarysignedContext):
        pass


    # Enter a parse tree produced by WdlParser#map_literal.
    def enterMap_literal(self, ctx:WdlParser.Map_literalContext):
        pass

    # Exit a parse tree produced by WdlParser#map_literal.
    def exitMap_literal(self, ctx:WdlParser.Map_literalContext):
        pass


    # Enter a parse tree produced by WdlParser#ifthenelse.
    def enterIfthenelse(self, ctx:WdlParser.IfthenelseContext):
        pass

    # Exit a parse tree produced by WdlParser#ifthenelse.
    def exitIfthenelse(self, ctx:WdlParser.IfthenelseContext):
        pass


    # Enter a parse tree produced by WdlParser#get_name.
    def enterGet_name(self, ctx:WdlParser.Get_nameContext):
        pass

    # Exit a parse tree produced by WdlParser#get_name.
    def exitGet_name(self, ctx:WdlParser.Get_nameContext):
        pass


    # Enter a parse tree produced by WdlParser#array_literal.
    def enterArray_literal(self, ctx:WdlParser.Array_literalContext):
        pass

    # Exit a parse tree produced by WdlParser#array_literal.
    def exitArray_literal(self, ctx:WdlParser.Array_literalContext):
        pass


    # Enter a parse tree produced by WdlParser#struct_literal.
    def enterStruct_literal(self, ctx:WdlParser.Struct_literalContext):
        pass

    # Exit a parse tree produced by WdlParser#struct_literal.
    def exitStruct_literal(self, ctx:WdlParser.Struct_literalContext):
        pass


    # Enter a parse tree produced by WdlParser#version.
    def enterVersion(self, ctx:WdlParser.VersionContext):
        pass

    # Exit a parse tree produced by WdlParser#version.
    def exitVersion(self, ctx:WdlParser.VersionContext):
        pass


    # Enter a parse tree produced by WdlParser#import_alias.
    def enterImport_alias(self, ctx:WdlParser.Import_aliasContext):
        pass

    # Exit a parse tree produced by WdlParser#import_alias.
    def exitImport_alias(self, ctx:WdlParser.Import_aliasContext):
        pass


    # Enter a parse tree produced by WdlParser#import_as.
    def enterImport_as(self, ctx:WdlParser.Import_asContext):
        pass

    # Exit a parse tree produced by WdlParser#import_as.
    def exitImport_as(self, ctx:WdlParser.Import_asContext):
        pass


    # Enter a parse tree produced by WdlParser#import_doc.
    def enterImport_doc(self, ctx:WdlParser.Import_docContext):
        pass

    # Exit a parse tree produced by WdlParser#import_doc.
    def exitImport_doc(self, ctx:WdlParser.Import_docContext):
        pass


    # Enter a parse tree produced by WdlParser#struct.
    def enterStruct(self, ctx:WdlParser.StructContext):
        pass

    # Exit a parse tree produced by WdlParser#struct.
    def exitStruct(self, ctx:WdlParser.StructContext):
        pass


    # Enter a parse tree produced by WdlParser#meta_kv.
    def enterMeta_kv(self, ctx:WdlParser.Meta_kvContext):
        pass

    # Exit a parse tree produced by WdlParser#meta_kv.
    def exitMeta_kv(self, ctx:WdlParser.Meta_kvContext):
        pass


    # Enter a parse tree produced by WdlParser#parameter_meta.
    def enterParameter_meta(self, ctx:WdlParser.Parameter_metaContext):
        pass

    # Exit a parse tree produced by WdlParser#parameter_meta.
    def exitParameter_meta(self, ctx:WdlParser.Parameter_metaContext):
        pass


    # Enter a parse tree produced by WdlParser#meta.
    def enterMeta(self, ctx:WdlParser.MetaContext):
        pass

    # Exit a parse tree produced by WdlParser#meta.
    def exitMeta(self, ctx:WdlParser.MetaContext):
        pass


    # Enter a parse tree produced by WdlParser#task_runtime_kv.
    def enterTask_runtime_kv(self, ctx:WdlParser.Task_runtime_kvContext):
        pass

    # Exit a parse tree produced by WdlParser#task_runtime_kv.
    def exitTask_runtime_kv(self, ctx:WdlParser.Task_runtime_kvContext):
        pass


    # Enter a parse tree produced by WdlParser#task_runtime.
    def enterTask_runtime(self, ctx:WdlParser.Task_runtimeContext):
        pass

    # Exit a parse tree produced by WdlParser#task_runtime.
    def exitTask_runtime(self, ctx:WdlParser.Task_runtimeContext):
        pass


    # Enter a parse tree produced by WdlParser#task_hints_kv.
    def enterTask_hints_kv(self, ctx:WdlParser.Task_hints_kvContext):
        pass

    # Exit a parse tree produced by WdlParser#task_hints_kv.
    def exitTask_hints_kv(self, ctx:WdlParser.Task_hints_kvContext):
        pass


    # Enter a parse tree produced by WdlParser#task_hints.
    def enterTask_hints(self, ctx:WdlParser.Task_hintsContext):
        pass

    # Exit a parse tree produced by WdlParser#task_hints.
    def exitTask_hints(self, ctx:WdlParser.Task_hintsContext):
        pass


    # Enter a parse tree produced by WdlParser#task_input.
    def enterTask_input(self, ctx:WdlParser.Task_inputContext):
        pass

    # Exit a parse tree produced by WdlParser#task_input.
    def exitTask_input(self, ctx:WdlParser.Task_inputContext):
        pass


    # Enter a parse tree produced by WdlParser#task_output.
    def enterTask_output(self, ctx:WdlParser.Task_outputContext):
        pass

    # Exit a parse tree produced by WdlParser#task_output.
    def exitTask_output(self, ctx:WdlParser.Task_outputContext):
        pass


    # Enter a parse tree produced by WdlParser#task_command.
    def enterTask_command(self, ctx:WdlParser.Task_commandContext):
        pass

    # Exit a parse tree produced by WdlParser#task_command.
    def exitTask_command(self, ctx:WdlParser.Task_commandContext):
        pass


    # Enter a parse tree produced by WdlParser#task_command_string_part.
    def enterTask_command_string_part(self, ctx:WdlParser.Task_command_string_partContext):
        pass

    # Exit a parse tree produced by WdlParser#task_command_string_part.
    def exitTask_command_string_part(self, ctx:WdlParser.Task_command_string_partContext):
        pass


    # Enter a parse tree produced by WdlParser#task_command_expr_part.
    def enterTask_command_expr_part(self, ctx:WdlParser.Task_command_expr_partContext):
        pass

    # Exit a parse tree produced by WdlParser#task_command_expr_part.
    def exitTask_command_expr_part(self, ctx:WdlParser.Task_command_expr_partContext):
        pass


    # Enter a parse tree produced by WdlParser#task_command_expr_with_string.
    def enterTask_command_expr_with_string(self, ctx:WdlParser.Task_command_expr_with_stringContext):
        pass

    # Exit a parse tree produced by WdlParser#task_command_expr_with_string.
    def exitTask_command_expr_with_string(self, ctx:WdlParser.Task_command_expr_with_stringContext):
        pass


    # Enter a parse tree produced by WdlParser#task_element.
    def enterTask_element(self, ctx:WdlParser.Task_elementContext):
        pass

    # Exit a parse tree produced by WdlParser#task_element.
    def exitTask_element(self, ctx:WdlParser.Task_elementContext):
        pass


    # Enter a parse tree produced by WdlParser#task.
    def enterTask(self, ctx:WdlParser.TaskContext):
        pass

    # Exit a parse tree produced by WdlParser#task.
    def exitTask(self, ctx:WdlParser.TaskContext):
        pass


    # Enter a parse tree produced by WdlParser#inner_workflow_element.
    def enterInner_workflow_element(self, ctx:WdlParser.Inner_workflow_elementContext):
        pass

    # Exit a parse tree produced by WdlParser#inner_workflow_element.
    def exitInner_workflow_element(self, ctx:WdlParser.Inner_workflow_elementContext):
        pass


    # Enter a parse tree produced by WdlParser#call_alias.
    def enterCall_alias(self, ctx:WdlParser.Call_aliasContext):
        pass

    # Exit a parse tree produced by WdlParser#call_alias.
    def exitCall_alias(self, ctx:WdlParser.Call_aliasContext):
        pass


    # Enter a parse tree produced by WdlParser#call_input.
    def enterCall_input(self, ctx:WdlParser.Call_inputContext):
        pass

    # Exit a parse tree produced by WdlParser#call_input.
    def exitCall_input(self, ctx:WdlParser.Call_inputContext):
        pass


    # Enter a parse tree produced by WdlParser#call_inputs.
    def enterCall_inputs(self, ctx:WdlParser.Call_inputsContext):
        pass

    # Exit a parse tree produced by WdlParser#call_inputs.
    def exitCall_inputs(self, ctx:WdlParser.Call_inputsContext):
        pass


    # Enter a parse tree produced by WdlParser#call_body.
    def enterCall_body(self, ctx:WdlParser.Call_bodyContext):
        pass

    # Exit a parse tree produced by WdlParser#call_body.
    def exitCall_body(self, ctx:WdlParser.Call_bodyContext):
        pass


    # Enter a parse tree produced by WdlParser#call_afters.
    def enterCall_afters(self, ctx:WdlParser.Call_aftersContext):
        pass

    # Exit a parse tree produced by WdlParser#call_afters.
    def exitCall_afters(self, ctx:WdlParser.Call_aftersContext):
        pass


    # Enter a parse tree produced by WdlParser#call_name.
    def enterCall_name(self, ctx:WdlParser.Call_nameContext):
        pass

    # Exit a parse tree produced by WdlParser#call_name.
    def exitCall_name(self, ctx:WdlParser.Call_nameContext):
        pass


    # Enter a parse tree produced by WdlParser#call.
    def enterCall(self, ctx:WdlParser.CallContext):
        pass

    # Exit a parse tree produced by WdlParser#call.
    def exitCall(self, ctx:WdlParser.CallContext):
        pass


    # Enter a parse tree produced by WdlParser#scatter.
    def enterScatter(self, ctx:WdlParser.ScatterContext):
        pass

    # Exit a parse tree produced by WdlParser#scatter.
    def exitScatter(self, ctx:WdlParser.ScatterContext):
        pass


    # Enter a parse tree produced by WdlParser#conditional.
    def enterConditional(self, ctx:WdlParser.ConditionalContext):
        pass

    # Exit a parse tree produced by WdlParser#conditional.
    def exitConditional(self, ctx:WdlParser.ConditionalContext):
        pass


    # Enter a parse tree produced by WdlParser#workflow_input.
    def enterWorkflow_input(self, ctx:WdlParser.Workflow_inputContext):
        pass

    # Exit a parse tree produced by WdlParser#workflow_input.
    def exitWorkflow_input(self, ctx:WdlParser.Workflow_inputContext):
        pass


    # Enter a parse tree produced by WdlParser#workflow_output.
    def enterWorkflow_output(self, ctx:WdlParser.Workflow_outputContext):
        pass

    # Exit a parse tree produced by WdlParser#workflow_output.
    def exitWorkflow_output(self, ctx:WdlParser.Workflow_outputContext):
        pass


    # Enter a parse tree produced by WdlParser#input.
    def enterInput(self, ctx:WdlParser.InputContext):
        pass

    # Exit a parse tree produced by WdlParser#input.
    def exitInput(self, ctx:WdlParser.InputContext):
        pass


    # Enter a parse tree produced by WdlParser#output.
    def enterOutput(self, ctx:WdlParser.OutputContext):
        pass

    # Exit a parse tree produced by WdlParser#output.
    def exitOutput(self, ctx:WdlParser.OutputContext):
        pass


    # Enter a parse tree produced by WdlParser#inner_element.
    def enterInner_element(self, ctx:WdlParser.Inner_elementContext):
        pass

    # Exit a parse tree produced by WdlParser#inner_element.
    def exitInner_element(self, ctx:WdlParser.Inner_elementContext):
        pass


    # Enter a parse tree produced by WdlParser#parameter_meta_element.
    def enterParameter_meta_element(self, ctx:WdlParser.Parameter_meta_elementContext):
        pass

    # Exit a parse tree produced by WdlParser#parameter_meta_element.
    def exitParameter_meta_element(self, ctx:WdlParser.Parameter_meta_elementContext):
        pass


    # Enter a parse tree produced by WdlParser#meta_element.
    def enterMeta_element(self, ctx:WdlParser.Meta_elementContext):
        pass

    # Exit a parse tree produced by WdlParser#meta_element.
    def exitMeta_element(self, ctx:WdlParser.Meta_elementContext):
        pass


    # Enter a parse tree produced by WdlParser#workflow.
    def enterWorkflow(self, ctx:WdlParser.WorkflowContext):
        pass

    # Exit a parse tree produced by WdlParser#workflow.
    def exitWorkflow(self, ctx:WdlParser.WorkflowContext):
        pass


    # Enter a parse tree produced by WdlParser#document_element.
    def enterDocument_element(self, ctx:WdlParser.Document_elementContext):
        pass

    # Exit a parse tree produced by WdlParser#document_element.
    def exitDocument_element(self, ctx:WdlParser.Document_elementContext):
        pass


    # Enter a parse tree produced by WdlParser#document.
    def enterDocument(self, ctx:WdlParser.DocumentContext):
        pass

    # Exit a parse tree produced by WdlParser#document.
    def exitDocument(self, ctx:WdlParser.DocumentContext):
        pass



del WdlParser