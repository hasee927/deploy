<script setup lang="tsx">
import { useTimeAgo } from '@/hooks/web/useTimeAgo'
import { ElRow, ElCol, ElSkeleton, ElCard, ElDivider, ElLink } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { ref, reactive, computed, unref } from 'vue'
import { formatTime, getGreeting, getCurrentDate, getDayOfWeek } from '@/utils'
import { Highlight } from '@/components/Highlight'
import {
	getCollectionRankingApi,
	getCollectionDataApi,
	getPayOutDataApi,
	getPayRankingApi,
	getPayPendingApi
} from '@/api/dashboard/workplace'
import { getFinanceApi } from '@/api/yinggao/finance/finance'
import type { Project, Dynamic, Team, Shortcuts } from '@/api/dashboard/workplace/types'
import avatar from '@/assets/imgs/avatar.jpg'
import { useAuthStore } from '@/store/modules/auth'
import { Table, TableColumn } from '@/components/Table'
import { BaseButton } from '@/components/Button'


const limit = 100
const { t } = useI18n()

const loading = ref(false)


	// 获取今日和昨天的统计数据
	const todayCollectionData = ref({})
	const yestCollectionData = ref({})

	const getCollectionDataAll = async () => {
		const res = await getCollectionDataApi().catch(() => { })
		if (res) {
			todayCollectionData.value = res.data.today
			yestCollectionData.value = res.data.yesterday
		}
	}

	getCollectionDataAll()
	
	
	
	
	// 获取今日和昨天的代付统计数据
	const todayPayOutData = ref({})
	const yestPayOutData = ref({})
	
	const getPayOutDataAll = async () => {
		const res = await getPayOutDataApi().catch(() => { })
		if (res) {
			todayPayOutData.value = res.data.today
			yestPayOutData.value = res.data.yesterday
		}
	}
	
	getPayOutDataAll()
	

	// 充值排行榜
	const dataList = ref([])
	const getMerchantColl = async () => {
		const jsonData = {
		  page: 1,
		  limit: limit
		}
		const res = await getFinanceApi(jsonData)
		if (res) {
			dataList.value = res.data
			collTotal.value = res.count || 0
		}
	}
	getMerchantColl()
	
	// 获取代付排行榜
	const page2 = ref(1)
	const payTotal = ref(0)
	const dataList2 = ref([])
	const getPayRanking = async () => {
		const jsonData = {
			page: unref(page2),
			limit: unref(limit)
		}
		
		const res = await getPayRankingApi(jsonData)
		if (res) {
			dataList2.value = res.data
			// payTotal.value = res.count || 0
			payTotal.value = 1000
		}
	}
	
	getPayRanking()


	// const handleCurrentChangePay = (val: number) => {
	//   page2.value = val
	//   getPayRanking()
	// }



	// 获取代收排行榜
	const page3 = ref(1)
	const collTotal = ref(0)
	const dataList3 = ref([])
	const getCollectionRanking = async () => {
		const jsonData = {
			page: unref(page3),
			limit: unref(limit)
		}
		
		const res = await getCollectionRankingApi(jsonData)
		if (res) {
			dataList3.value = res.data
			collTotal.value = res.count || 0
		}
	}
	
	getCollectionRanking()


	// const handleCurrentChangeColl = (val: number) => {
	//   page3.value = val
	//   getCollectionRanking()
	// }


	const pending_total_amount = ref(0)
	const getPayPending = async () => {
		const res = await getPayPendingApi()
		if (res) {
			pending_total_amount.value = res.data
		}
	}
	getPayPending()



</script>


<template>
	<div class="bg-[var(--app-content-bg-color)] flex-grow">
		<div class="mx-20px mt-20px">
			<ElRow :gutter="20" justify="space-between">
				<ElCol :xl="16" :lg="16" :md="24" :sm="24" :xs="24" class="mb-20px">
					<ElCard shadow="never"  style="background: #edfbff;">
						<template #header>
							<div class="flex justify-between" style="font-size: 20px; font-weight: bolder;">
								代收数据情况
							</div>
						</template>
						<ElSkeleton :loading="loading" animated>
							<ElRow>
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代收</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{todayCollectionData.total_amount}}</span>
												<!-- <span>68634472</span> -->
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代收</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{yestCollectionData.total_amount}}</span>
												<!-- <span>136225472</span> -->
											</div>

										</div>
									</ElCard>
								</ElCol>
								
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代收成功单数</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{todayCollectionData.count}}</span>
												<!-- <span>106554</span> -->
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代收成功单数</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{yestCollectionData.count}}</span>
												<!-- <span>265597</span> -->
											</div>
								
										</div>
									</ElCard>
								</ElCol>
								
								
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代收提交数</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{todayCollectionData.total}}</span>
												<!-- <span>212286</span> -->
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代收提交数</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{yestCollectionData.total}}</span>
												<!-- <span>372262</span> -->
											</div>
								
										</div>
									</ElCard>
								</ElCol>
								
								
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代收成功率</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{todayCollectionData.success_rate}}</span>
												<!-- <span>55.58%</span> -->
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代收成功率</span>
											</div>
											<div class="flex items-center justify-center">
												<span>{{yestCollectionData.success_rate}}</span>
												<!-- <span>50.52%</span> -->
											</div>
								
										</div>
									</ElCard>
								</ElCol>
								
								
							</ElRow>
						</ElSkeleton>
					</ElCard>



					<ElCard shadow="never" style="background: #e7f2ff;">
						<template #header>
							<div class="flex justify-between" style="font-size: 20px; font-weight: bolder;">
								代付数据情况
							</div>
						</template>
						<ElSkeleton :loading="loading" animated>
							<ElRow>
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代付</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>30790409.15</span> -->
												<span>{{todayPayOutData.total_amount}}</span>
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代付</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>64739072.41</span> -->
												<span>{{yestPayOutData.total_amount}}</span>
											</div>
					
										</div>
									</ElCard>
								</ElCol>
								
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代付成功单数</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>2694</span> -->
												<span>{{todayPayOutData.count}}</span>
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代付成功单数</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>2945</span> -->
												<span>{{yestPayOutData.count}}</span>
											</div>
								
										</div>
									</ElCard>
								</ElCol>
								
								
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代付提交数</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>30790</span> -->
												<span>{{todayPayOutData.total}}</span>
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代付提交数</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>6974521</span> -->
												<span>{{yestPayOutData.total}}</span>
											</div>
								
										</div>
									</ElCard>
								</ElCol>
								
								
								<ElCol :xl="6">
									<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
										<div style="font-weight: bold;">
											<div class="flex items-center justify-center">
												<span>今日-代付成功率</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>36.15%</span> -->
												<span>{{todayPayOutData.success_rate}}</span>
											</div>
											<div style="margin-top: 10px;"></div>
											<div class="flex items-center justify-center">
												<span>昨日-代付成功率</span>
											</div>
											<div class="flex items-center justify-center">
												<!-- <span>37.57%</span> -->
												<span>{{yestPayOutData.success_rate}}</span>
											</div>
								
										</div>
									</ElCard>
								</ElCol>
								
								
							</ElRow>
						</ElSkeleton>
					</ElCard>
					
					
				</ElCol>
				
				
				
				
				<ElCol :xl="8" :lg="8" :md="24" :sm="24" :xs="24" class="mb-20px">
					<ElCard shadow="never">
						<template #header>
							<span style="font-size: 20px; font-weight: bolder;">账单数据情况</span>
						</template>
						<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
							<div style="font-weight: bold;">
								<div class="flex items-center justify-center">
									<span>代付账号余额</span>
								</div>
								<div class="flex items-center justify-center">
									<span>0</span>
								</div>
								<div style="margin-top: 10px;"></div>
								<div class="flex items-center justify-center">
									<span>代付Pending</span>
								</div>
								<div class="flex items-center justify-center">
									<span>{{pending_total_amount}}</span>
								</div>
														
							</div>
						</ElCard>
						
						<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
							<div style="font-weight: bold;">
								<div class="flex items-center justify-center">
									<span>代付冻结总金额</span>
								</div>
								<div class="flex items-center justify-center">
									<span>0</span>
								</div>
								<div style="margin-top: 10px;"></div>
								<div class="flex items-center justify-center">
									<span>结算冻结总金额</span>
								</div>
								<div class="flex items-center justify-center">
									<span>0</span>
								</div>
														
							</div>
						</ElCard>
						
						<ElCard shadow="hover"  style="background-color: #00aaff; color: #ffffff;">
							<div style="font-weight: bold;">
								<div class="flex items-center justify-center">
									<span>可结算余额</span>
								</div>
								<div class="flex items-center justify-center">
									<span>0</span>
								</div>														
							</div>
						</ElCard>
						
					</ElCard>
				</ElCol>
				
				
				<!-- ================================================================ -->
				<ElCol :xl="8" :lg="8" :md="24" :sm="24" :xs="24" class="mb-20px">
				  <ElCard shadow="never">
				    <template #header>
				      <span>今日-充值排行榜</span>
				    </template>
				    <ElSkeleton :loading="loading" animated>
						<el-table :data="dataList" stripe style="width: 100%">
						  <el-table-column prop="change_fund" label="total"  />
						  <el-table-column prop="merchant_id" label="商户"  />
						</el-table>
						
						<!-- <div class="demo-pagination-block" v-show="dataList.length">
							<el-pagination
								v-model:current-page="page3"
								v-model:page-size="limit"
								layout="prev, pager, next"
								:total="collTotal"
								@current-change="handleCurrentChangeColl"
							/>
						</div> -->
				    </ElSkeleton>
				  </ElCard>
				</ElCol>
				
				<ElCol :xl="8" :lg="8" :md="24" :sm="24" :xs="24" class="mb-20px">
				  <ElCard shadow="never">
				    <template #header>
				      <span>今日-代付排行榜</span>
				    </template>
				    <ElSkeleton :loading="loading" animated>
				     
						<el-table :data="dataList2" stripe style="width: 100%">
					      <el-table-column prop="total" label="total"  />
					      <el-table-column prop="merchant_id" label="商户"  />
					      <el-table-column prop="today_count" label="订单数" />
						  <el-table-column prop="today_success_rate" label="成功率" />
					    </el-table>
						
						<!-- <div class="demo-pagination-block" v-show="dataList2.length">
							<el-pagination
								v-model:current-page="page2"
								v-model:page-size="limit"
								layout="prev, pager, next"
								:total="payTotal"
								@current-change="handleCurrentChangePay"
							/>
						</div> -->
					  
				    </ElSkeleton>
				  </ElCard>
				</ElCol>
				
				
				<ElCol :xl="8" :lg="8" :md="24" :sm="24" :xs="24" class="mb-20px">
				  <ElCard shadow="never">
				    <template #header>
				      <span>今日-代收排行榜</span>
				    </template>
				    <ElSkeleton :loading="loading" animated>
						<el-table :data="dataList3" stripe style="width: 100%">
						  <el-table-column prop="total" label="total"  />
						  <el-table-column prop="merchant_id" label="商户"  />
						  <el-table-column prop="today_count" label="订单数" />
						  <el-table-column prop="today_success_rate" label="成功率" />
						</el-table>
						
						<!-- <div class="demo-pagination-block" v-show="dataList3.length">
							<el-pagination
								v-model:current-page="page3"
								v-model:page-size="limit"
								layout="prev, pager, next"
								:total="collTotal"
								@current-change="handleCurrentChangeColl"
							/>
						</div> -->
				    </ElSkeleton>
				  </ElCard>
				</ElCol>
			</ElRow>
		</div>
	</div>
</template>


<style scoped>

	.demo-pagination-block {
	  margin-top: 20px;
	}
</style>