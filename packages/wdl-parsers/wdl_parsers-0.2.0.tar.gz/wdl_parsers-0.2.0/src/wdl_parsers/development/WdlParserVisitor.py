# Generated from WdlParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .WdlParser import WdlParser
else:
    from WdlParser import WdlParser

# This class defines a complete generic visitor for a parse tree produced by WdlParser.

class WdlParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by WdlParser#map_type.
    def visitMap_type(self, ctx:WdlParser.Map_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#array_type.
    def visitArray_type(self, ctx:WdlParser.Array_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#pair_type.
    def visitPair_type(self, ctx:WdlParser.Pair_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#type_base.
    def visitType_base(self, ctx:WdlParser.Type_baseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#wdl_type.
    def visitWdl_type(self, ctx:WdlParser.Wdl_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#unbound_decls.
    def visitUnbound_decls(self, ctx:WdlParser.Unbound_declsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#bound_decls.
    def visitBound_decls(self, ctx:WdlParser.Bound_declsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#any_decls.
    def visitAny_decls(self, ctx:WdlParser.Any_declsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#number.
    def visitNumber(self, ctx:WdlParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#string_part.
    def visitString_part(self, ctx:WdlParser.String_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#string_expr_part.
    def visitString_expr_part(self, ctx:WdlParser.String_expr_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#string_expr_with_string_part.
    def visitString_expr_with_string_part(self, ctx:WdlParser.String_expr_with_string_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#string.
    def visitString(self, ctx:WdlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#primitive_literal.
    def visitPrimitive_literal(self, ctx:WdlParser.Primitive_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#expr.
    def visitExpr(self, ctx:WdlParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#infix0.
    def visitInfix0(self, ctx:WdlParser.Infix0Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#infix1.
    def visitInfix1(self, ctx:WdlParser.Infix1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#lor.
    def visitLor(self, ctx:WdlParser.LorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#infix2.
    def visitInfix2(self, ctx:WdlParser.Infix2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#land.
    def visitLand(self, ctx:WdlParser.LandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#eqeq.
    def visitEqeq(self, ctx:WdlParser.EqeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#lt.
    def visitLt(self, ctx:WdlParser.LtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#infix3.
    def visitInfix3(self, ctx:WdlParser.Infix3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#gte.
    def visitGte(self, ctx:WdlParser.GteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#neq.
    def visitNeq(self, ctx:WdlParser.NeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#lte.
    def visitLte(self, ctx:WdlParser.LteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#gt.
    def visitGt(self, ctx:WdlParser.GtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#add.
    def visitAdd(self, ctx:WdlParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#sub.
    def visitSub(self, ctx:WdlParser.SubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#infix4.
    def visitInfix4(self, ctx:WdlParser.Infix4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#mod.
    def visitMod(self, ctx:WdlParser.ModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#mul.
    def visitMul(self, ctx:WdlParser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#divide.
    def visitDivide(self, ctx:WdlParser.DivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#infix5.
    def visitInfix5(self, ctx:WdlParser.Infix5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#expr_infix5.
    def visitExpr_infix5(self, ctx:WdlParser.Expr_infix5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#pair_literal.
    def visitPair_literal(self, ctx:WdlParser.Pair_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#apply.
    def visitApply(self, ctx:WdlParser.ApplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#expression_group.
    def visitExpression_group(self, ctx:WdlParser.Expression_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#primitives.
    def visitPrimitives(self, ctx:WdlParser.PrimitivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#left_name.
    def visitLeft_name(self, ctx:WdlParser.Left_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#at.
    def visitAt(self, ctx:WdlParser.AtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#negate.
    def visitNegate(self, ctx:WdlParser.NegateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#unirarysigned.
    def visitUnirarysigned(self, ctx:WdlParser.UnirarysignedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#map_literal.
    def visitMap_literal(self, ctx:WdlParser.Map_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#ifthenelse.
    def visitIfthenelse(self, ctx:WdlParser.IfthenelseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#get_name.
    def visitGet_name(self, ctx:WdlParser.Get_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#array_literal.
    def visitArray_literal(self, ctx:WdlParser.Array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#struct_literal.
    def visitStruct_literal(self, ctx:WdlParser.Struct_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#version.
    def visitVersion(self, ctx:WdlParser.VersionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#import_alias.
    def visitImport_alias(self, ctx:WdlParser.Import_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#import_as.
    def visitImport_as(self, ctx:WdlParser.Import_asContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#import_doc.
    def visitImport_doc(self, ctx:WdlParser.Import_docContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#struct.
    def visitStruct(self, ctx:WdlParser.StructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#meta_kv.
    def visitMeta_kv(self, ctx:WdlParser.Meta_kvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#parameter_meta.
    def visitParameter_meta(self, ctx:WdlParser.Parameter_metaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#meta.
    def visitMeta(self, ctx:WdlParser.MetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_runtime_kv.
    def visitTask_runtime_kv(self, ctx:WdlParser.Task_runtime_kvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_runtime.
    def visitTask_runtime(self, ctx:WdlParser.Task_runtimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_hints_kv.
    def visitTask_hints_kv(self, ctx:WdlParser.Task_hints_kvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_hints.
    def visitTask_hints(self, ctx:WdlParser.Task_hintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_input.
    def visitTask_input(self, ctx:WdlParser.Task_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_output.
    def visitTask_output(self, ctx:WdlParser.Task_outputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_command.
    def visitTask_command(self, ctx:WdlParser.Task_commandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_command_string_part.
    def visitTask_command_string_part(self, ctx:WdlParser.Task_command_string_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_command_expr_part.
    def visitTask_command_expr_part(self, ctx:WdlParser.Task_command_expr_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_command_expr_with_string.
    def visitTask_command_expr_with_string(self, ctx:WdlParser.Task_command_expr_with_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task_element.
    def visitTask_element(self, ctx:WdlParser.Task_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#task.
    def visitTask(self, ctx:WdlParser.TaskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#inner_workflow_element.
    def visitInner_workflow_element(self, ctx:WdlParser.Inner_workflow_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#call_alias.
    def visitCall_alias(self, ctx:WdlParser.Call_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#call_input.
    def visitCall_input(self, ctx:WdlParser.Call_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#call_inputs.
    def visitCall_inputs(self, ctx:WdlParser.Call_inputsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#call_body.
    def visitCall_body(self, ctx:WdlParser.Call_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#call_afters.
    def visitCall_afters(self, ctx:WdlParser.Call_aftersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#call_name.
    def visitCall_name(self, ctx:WdlParser.Call_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#call.
    def visitCall(self, ctx:WdlParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#scatter.
    def visitScatter(self, ctx:WdlParser.ScatterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#conditional.
    def visitConditional(self, ctx:WdlParser.ConditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#workflow_input.
    def visitWorkflow_input(self, ctx:WdlParser.Workflow_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#workflow_output.
    def visitWorkflow_output(self, ctx:WdlParser.Workflow_outputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#input.
    def visitInput(self, ctx:WdlParser.InputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#output.
    def visitOutput(self, ctx:WdlParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#inner_element.
    def visitInner_element(self, ctx:WdlParser.Inner_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#parameter_meta_element.
    def visitParameter_meta_element(self, ctx:WdlParser.Parameter_meta_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#meta_element.
    def visitMeta_element(self, ctx:WdlParser.Meta_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#workflow.
    def visitWorkflow(self, ctx:WdlParser.WorkflowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#document_element.
    def visitDocument_element(self, ctx:WdlParser.Document_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WdlParser#document.
    def visitDocument(self, ctx:WdlParser.DocumentContext):
        return self.visitChildren(ctx)



del WdlParser