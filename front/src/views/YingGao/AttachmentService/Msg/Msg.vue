<template>

	<el-card style="width: 100%; height: 100%;">

		<el-form  ref="ruleFormRef" style="margin-top: 30px;max-width: 800px; margin-left: 160px;" :model="ruleForm"
			:rules="rules" label-width="auto" class="demo-ruleForm" :size="formSize" status-icon>

			<el-form-item label="通知对象" prop="msgType">
				<el-select v-model="ruleForm.msgType" placeholder="请选择">
					<el-option label="商户" value="1" />
					<el-option label="渠道" value="2"/>
				</el-select>
			</el-form-item>
			<el-form-item label="消息内容" prop="orderNo">
				<!-- <el-input v-model="ruleForm.orderNo" /> -->
				<el-input
				  v-model="ruleForm.textarea"
				  style="width: 800px"
				  :autosize="{ minRows: 10, maxRows: 1000 }"
				  type="textarea"
				  placeholder="请输入消息内容"
				/>
			</el-form-item>
			

			<el-form-item>
				<el-button type="primary" @click="submit(ruleFormRef)">
					发送
				</el-button>
			</el-form-item>
		</el-form>

		
		

	</el-card>

</template>

<script lang="ts" setup>
	import { reactive, ref } from 'vue'
	import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
	import { senderMsgApi } from '@/api/yinggao/AttachmentService/msg'
	import { ElForm, ElMessage, ElMessageBox, ElTree } from 'element-plus'
	import CryptoJS from 'crypto-js'
	
	interface RuleForm {
		msgType : string
		textarea : string
		
	}

	
	const formSize = ref<ComponentSize>('default')
	const ruleFormRef = ref<FormInstance>()

	const ruleForm = reactive<RuleForm>({
		msgType: '1',
		textarea: '',
	
	})
	


	const rules = reactive<FormRules<RuleForm>>({
		

	})



	const submit = async () => {
		ElMessageBox.confirm(
			'确定发送消息?',
			'系统提示',
			{
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
			}).then(async () => {
				const res = await senderMsgApi(ruleForm)
				if (res){
					ElMessage({
						type: 'success',
						message: '发送成功',
					})
					ruleForm.textarea = ''
				}

				
			}).catch(() => {
				ElMessage({
					type: 'info',
					message: '取消发送',
				})
			})

	}


	
	
</script>

<style scoped lang="less">
	.el-button {
		margin-left: 106px;
	}
</style>