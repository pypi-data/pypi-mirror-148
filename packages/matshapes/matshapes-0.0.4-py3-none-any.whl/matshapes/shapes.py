
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib.gridspec as grids
from matplotlib.gridspec import GridSpec as Grids
from matplotlib.markers import MarkerStyle
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import matplotlib.pyplot as plt

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

semicircles = [MarkerStyle('o', fillstyle='left'), MarkerStyle('o', fillstyle='right')]

def ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse), [mean_x-scale_x, mean_x+scale_x, mean_y-scale_y, mean_y+scale_y]

#### inc_dec_fc_bar --> stacked_bar
def stacked_bar(ax, dom_name, n_female, n_male, width, title, n_fc, position, dif_v):
    xs, w, cs = np.arange(len(dom_name)), width, ['dodgerblue','coral','fuchsia','lime'] #['tab:blue','tab:pink','tab:orange','deepskyblue']
    b, ls = 0, [' '*9+r'$+\    \ -$', ' '*9+r'$-\    \ -$', ' '*9+r'$+\    \ +$', ' '*9+r'$-\    \ +$']

    nf, nm = [], []
    for x, vm, vf, d in zip(xs, n_male, n_female, dif_v):
        b = 0
        [[nf.append(np.isin(vf, j).sum()), nm.append(np.isin(vm, j).sum())] for j in range(4)]
        for m,f in zip(vm, vf):
            ax.bar(x-w/2, 1, width=w, ec='black', color=cs[m], bottom=b)
            ax.bar(x+w/2, 1, width=w, ec='black', color=cs[f], bottom=b, hatch='////')
            b += 1
        # ax.text(x-w*1.5, b+0.04, '{:.2f}'.format(d), fontsize=10, rotation=24)
        
    [ax.bar(x-w/2, 0, width=w, color=cs[j], ec='black', label='  ', bottom=0) for j in range(4)]
    [ax.bar(x+w/2, 0, width=w, color=cs[j], ec='black', label=ls[j], bottom=0, hatch='////') for j in range(4)]

    leg1 = ax.legend(title='Male  Female  FC  corr', ncol=2, columnspacing=0.66, handletextpad=0.18, handlelength=1.4, fontsize=12, title_fontsize=12) # 第一个标签
    leg1._legend_box.align = "left"

    nf, nm = np.array(nf).reshape(-1,4), np.array(nm).reshape(-1,4)
    
    #### legend (percent)
    in_i = [j for j,k in enumerate(dom_name) if k[:2]==k[-2:]] ## within idx
    btn_i = [j for j,k in enumerate(dom_name) if k[:2]!=k[-2:]] ## between idx

    f_n, m_n = nf.sum(axis=0), nm.sum(axis=0) #### total number
    f_in, m_in = nf[in_i].sum(axis=0), nm[in_i].sum(axis=0) #### 个数
    f_btn, m_btn = nf[btn_i].sum(axis=0), nm[btn_i].sum(axis=0) #### 个数
    h0, l0 = ax.get_legend_handles_labels()
    l0 = ['{:d} ({:d} | {:d})'.format(total, in_n, btn_n) for total, in_n, btn_n in\
        zip(np.hstack([m_n, f_n]), np.hstack([m_in, f_in]),np.hstack([m_btn, f_btn]))]
    leg2 = ax.legend(h0, l0, ncol=2, loc=(position[0], position[1]), columnspacing=0.18,\
        title='FC number (within | between domains)', handletextpad=0.18, handlelength=1.4, fontsize=12, title_fontsize=12)

    h1, l1 = ax.get_legend_handles_labels()
    l1 = ['{:.1f}% ({:.1f}% | {:.1f}%)'.format(total*100/n_fc, in_n*100/n_fc, btn_n*100/n_fc) for total, in_n, btn_n in\
        zip(np.hstack([m_n, f_n]), np.hstack([m_in, f_in]),np.hstack([m_btn, f_btn]))]
    leg3 = ax.legend(h1, l1, ncol=2, loc=(position[2], position[3]), columnspacing=0.18,\
        title='Percentage (within | between domains)', handletextpad=0.18, handlelength=1.4, fontsize=12, title_fontsize=12)
    ax.add_artist(leg1), ax.add_artist(leg2)
    
    # for j in range(len(dom_name)):
    #     if dom_name[j][:2] == dom_name[j][-2:]: dom_name[j] = '*' + dom_name[j]
    ax.set_xticks(xs), ax.set_xticklabels(dom_name), ax.set_title(title, weight='bold')
    ax.set_yticks(np.arange(0,20,2)), ax.set_yticklabels(np.arange(0,20,2))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.set_xlim([-1, len(dom_name)]), ax.set_ylabel('FC number', weight='bold')
    plt.tight_layout()



# # from mpl_toolkits.axes_grid1 import ImageGrid
# import numpy as np
# from numpy import *
# from collections import *
# from shapes import *
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# from matplotlib.patches import Rectangle
# from matplotlib import ticker
# from matplotlib.ticker import FormatStrFormatter
# import matplotlib.pyplot as plt
# from scipy.stats import ttest_rel
# from nilearn import plotting
# from nilearn import image
# from orange3 import *
# import os

# ## global settings
# plt.rcParams['font.sans-serif']='Times New Roman'
# plt.rcParams.update({'axes.titlesize':'20', 'axes.labelsize':'16',\
#      'xtick.labelsize': '12', 'ytick.labelsize': '12', "font.weight": "bold"})

# ########################
# def load_all_result(args):
#     pt = args.result_path
#     n_ic = 55
#     n_feat, percent = 300, '6'
#     accs = [np.loadtxt(f'{pt}/AllFC/{k}_mean.txt') for k in ['f','m']]
#     main_f, main_m, ind_f, ind_m = np.loadtxt(f'{pt}/main_f.txt'), np.loadtxt(f'{pt}/main_m.txt'), np.loadtxt(f'{pt}/ind_f.txt'), np.loadtxt(f'{pt}/ind_m.txt')
#     effc, ave_acc = np.loadtxt(f'{pt}/efficiency.txt'), np.loadtxt(f'{pt}/overacc.txt')
#     i012, m012, s012, cp012 = load_impfc_mean_std_cp(pt, percent, n_feat)
#     net = get_brainnet(n_ic)
#     dom_names = list(net.keys())
#     dom_idx, ic_name = get_node_idx_name(net)
#     fc_name = get_fc_names(n_ic, dom_idx, ic_name, False)
#     cp_f_fi = np.loadtxt(f'{pt}/fc_corrs/fi_cp_f.txt')[:,0]
#     cp_m_fi = np.loadtxt(f'{pt}/fc_corrs/fi_cp_m.txt')[:,0]
#     cp_f_rt = np.loadtxt(f'{pt}/fc_corrs/rt_cp_f.txt')[:,0]
#     cp_m_rt = np.loadtxt(f'{pt}/fc_corrs/rt_cp_m.txt')[:,0]
#     cp_f_nm = np.loadtxt(f'{pt}/fc_corrs/nm_cp_f.txt')[:,0]
#     cp_m_nm = np.loadtxt(f'{pt}/fc_corrs/nm_cp_m.txt')[:,0]
#     return accs, main_f, main_m, ind_f, ind_m, effc, ave_acc, i012, m012, s012, cp012, net, dom_names, dom_idx, ic_name, fc_name, cp_f_fi, cp_f_nm, cp_f_rt, cp_m_fi, cp_m_nm, cp_m_rt

# def get_brainnet(n_ic):
#     if n_ic == 21:
#         nets = {'AT':[6], 'AU':[18], 'CB':[16], 'CC':[10,14,17,22], 'DM':[1,8,15,21],\
#             'FP':[7], 'SC':[19], 'SM':[3,11,12,13], 'VI':[2,5,9,20]}
#     else: # 45,25,57,64,2, 57(DM)->CC, 53(VI)->DM, 60(CB)->VI
#         nets = {'AT':[35,52], 'AU':[3,10,23,49], 'CB':[18,24,58],\
#             'CC':[12,14,16,19,22,26,27,29,30,32,34,38,41,46,48,50,57,63,64,93],\
#                 'DM':[6,8,11,20,37,53], 'FP':[13,25], 'SC':[39], 'SM':[7,21,28,31,33,36,40],\
#                     'VI':[2,4,5,9,15,17,42,43,45,60]}
#     return nets

# def seq2np_idx(idx):
#     """e.g., [1,4,8,3] --> [0,2,3,1]"""
#     i = np.argsort(idx) # sort_idx = idx[i]
#     ii = np.argsort(i) # idx = sort_idx[ii], replace sort_idx by [0,1,2,3,...]
#     np_i = np.arange(len(idx))
#     return np_i[ii]

# def get_node_idx_name(brain_net):
#     """IC idx to numpy idx and IC name"""
#     ic_name, ic_id = list(brain_net.keys()), list(brain_net.values())
#     ic_idx = list(seq2np_idx(np.hstack(ic_id)))
#     idx = [] # mat idx to np idx
#     for i in ic_id:
#         net = [ic_idx.pop(0) for _ in range(len(i))]
#         idx.append(net)
#     ns = [f'{n} ({jj})' for n,j in zip(ic_name, ic_id) for jj in j]
#     return idx, np.array(ns) # matched, idx is clustered by same domain

# def load_accs(n_ic, date):
#     accs = [np.loadtxt(f'age-{n_ic}-{date}/{s}_means.txt') for s in ['f','m']]
#     return accs

# def load_impfc_mean_std_cp(path, percent, n_feat):
#     """important FC's strength (mean, std) and correlation with age"""
#     pt, sex = f'{path}/fc_corrs/', ['f','m']
#     i012 = [np.loadtxt(f'{path}/AllFC/AgeingRelatedFC/{n_feat}-{s}_{percent}.txt', dtype=np.int32) for s in sex+['c']]
#     m012 = [np.loadtxt(f'{path}/fc_corrs/mean-{s}.txt') for s in sex]
#     s012 = [np.loadtxt(f'{path}/fc_corrs/std-{s}.txt') for s in sex]
#     cp012 = [np.loadtxt(f'{path}/fc_corrs/corr-{s}.txt').reshape(-1, 1) for s in sex]
#     return i012, m012, s012, cp012

# def get_sorted_node_name(node_idx, node_name):
#     """sort node name based on IC number"""
#     name = node_name[np.argsort(np.hstack(node_idx))]
#     return name

# def get_fc_names(n_ic, dom_idx, node_names, with_idx=True):
#     name = get_sorted_node_name(dom_idx, node_names)
#     mat = []
#     if with_idx:
#         [mat.append(f'{i}-{j}') for i in name for j in name]
#     else:
#         [mat.append(f'{i[:2]}-{j[:2]}') for i in name for j in name]
#     mat = np.array(mat, dtype=str).reshape(n_ic, n_ic)
#     mask = np.tril(np.ones_like(mat, dtype=np.int32), k=-1) > 0.5
#     return mat[mask]

# def tendency(ax, x, y, e, color, label):
#     ax.plot(x, y, color=color[0], label=label, lw=4)
#     ax.fill_between(x, y-e/10, y+e/10, color=color[1], alpha=0.5)

# def fcidx2dom(fc_idx, fc_name):
#     """ FC's idx to network """
#     dom = defaultdict(list)
#     for i in fc_idx:
#         a,b = fc_name[i].split('-')
#         name = sorted([f'{a}-{b}', f'{b}-{a}']) # A-B, B-A
#         dom[name[0]].append(i)
#     return OrderedDict(sorted(dom.items()))

# def four_behaviors(idx, cor, fc):
#     """ Four patterns of FC behavior """
#     p,n,u,d = fc>0, fc<0, cor>0, cor<0
#     pd, nd, pu, nu = p&d, n&d, p&u, n&u
#     return [idx[pd], idx[nd], idx[pu], idx[nu]]

# def four_behaviors_idx(cor, fc):
#     """idx: single idx"""
#     p_de, n_de, p_in, n_in = ((fc>0) & (cor<0)), ((fc<0) & (cor<0)),\
#         ((fc>0) & (cor>0)), ((fc<0) & (cor>0)) # + de, - de, + in, - in
#     i = 0 if p_de else 1 if n_de else 2 if p_in else 3
#     return [i]

# def dom2behaviors(dom, corr, fc):
#     """ divide FC in each dom into 4 patterns """
#     dom_behavior = dom.copy()
#     for k in dom:
#         idx = np.array(dom[k])
#         behavior = four_behaviors(idx, corr[idx], fc[idx])
#         dom_behavior[k] = behavior
#     return dom_behavior

# def behavior2idx(behavior, corr, fc):
#     """ convert fc behavior in each dom to pattern number for female and male"""
#     A, B = defaultdict(list), defaultdict(list)
#     for k in behavior:
#         for i, v in enumerate(behavior[k]):
#             n = len(v)
#             if n > 0:
#                 A[k] += [i]*n
#                 for j in v: B[k] += four_behaviors_idx(corr[j], fc[j])
#     return A, B

# def count_inc_dec_fc2dom(idx, cor, strth, dom_idx, ic_name, percent):
#     cor_sign, fc_sign = np.sign(cor[:,0]), np.sign(strth[0])
#     fc_name = get_fc_names(55, dom_idx, ic_name, False)
#     dom = defaultdict(list)
#     for i in idx:
#         a,b = fc_name[i].split('-')
#         name = sorted([f'{a}-{b}', f'{b}-{a}']) # A-B, B-A
#         if name[0] in dom or name[1] in dom: dom[name[0]].append(i)
#         else: dom[name[0]].append(i)
#     count = []
#     for key in dom:
#         count.append(count_inc_dec_fc(fc_sign[dom[key]], cor_sign[dom[key]], n=len(idx), percent=percent))
#     return dom, count

# def count_inc_dec_fc(idx, sign, cor, n=None, percent=True):
#     """four types of behaviors"""
#     if n is None: n = len(sign)
#     p_dec, n_dec, p_inc, n_inc = ((sign>0) & (cor<0)), ((sign<0) & (cor<0)),\
#         ((sign>0) & (cor>0)), ((sign<0) & (cor>0))
#     count = [v.sum()/n if percent else v.sum() for v in [p_dec, n_dec, p_inc, n_inc]]
#     return count

# def inc_dec_fc2dom_idx(dom, strth, combine=False):
#     if combine:
#         idx_dom = defaultdict(list)
#         for k in dom:
#             if k[:2] == k[-2:]: idx_dom['in'] += dom[k]
#             else: idx_dom['btn'] += dom[k]
#     else: idx_dom = dom.copy()
#     final_dom = defaultdict(list)
#     for k in idx_dom:
#         v = np.array(idx_dom[k])
#         sign = np.sign(strth[0][v])
#         final_dom[k].append(v[sign > 0]), final_dom[k].append(v[sign < 0])
#     return final_dom

# def inc_dec_fc2dom(dom, strth):
#     dom_traj = dom.copy()
#     for k in dom:
#         v = dom[k]
#         p, n = strth[:,v[0]].mean(axis=1) if len(v[0]) else [], strth[:,v[1]].mean(axis=1) if len(v[1]) else []
#         dom_traj[k] = [p, n]
#     return dom_traj

# def cor_sim_dif(dom, cor_f, cor_m, sex):
#     """ FC Sim or FC dif between F & M in each domain """
#     values = dom.copy()
#     for k in dom:
#         i = dom[k]
#         if sex == 0: v = ((cor_f[i] - cor_m[i]) * np.sign(cor_f[i])).sum()
#         elif sex == 1: v = ((cor_m[i] - cor_f[i]) * np.sign(cor_m[i])).sum()
#         else: v = (1 - np.abs(cor_f[i] - cor_m[i])).sum()
#         values[k] = v
#     return values

# def cor_sim_dif_(dom, cor_f, cor_m, sex):
#     """ FC Sim or FC dif between F & M in each domain """
#     values = dom.copy()
#     for k in dom:
#         ii, vs = dom[k], []
#         for i in ii:
#             if len(i):
#                 if sex == 0: v = ((cor_f[i] - cor_m[i]) * np.sign(cor_f[i])).sum()
#                 elif sex == 1: v = ((cor_m[i] - cor_f[i]) * np.sign(cor_m[i])).sum()
#                 else: v = (1 - np.abs(cor_f[i] - cor_m[i])).sum()
#             else: v = 0
#             vs.append(v)
#         values[k] = np.array(vs)
#     return values

# def select_fc(fc_idx, cor_f, cor_m, sex, n=10, base=0.5, total=False):
#     """select the most similar or different fc"""
#     cf, cm = cor_f[fc_idx], cor_m[fc_idx]
#     if sex == 0:
#         idx = fc_idx[np.where(np.abs(cf) > base)[0]]
#         i = np.argsort(-1 * (cor_f[idx]-cor_m[idx]) * np.sign(cor_f[idx]))
#         if total: j = np.argsort(-1 * (cor_f[fc_idx]-cor_m[fc_idx]) * np.sign(cor_f[fc_idx]))
#     elif sex == 1:
#         idx = fc_idx[np.where(np.abs(cm) > base)[0]]
#         i = np.argsort(-1 * (cor_m[idx]-cor_f[idx]) * np.sign(cor_m[idx]))
#         if total: j = np.argsort(-1 * (cor_m[fc_idx]-cor_f[fc_idx]) * np.sign(cor_m[fc_idx]))
#     else:
#         idx = fc_idx[np.where((np.abs(cf) > base) & (np.abs(cm) > base))[0]]
#         i = np.argsort(np.abs(cor_f[idx]-cor_m[idx]))
#         if total: j = np.argsort(np.abs(cor_f[fc_idx]-cor_m[fc_idx]))
#     return idx[i[:n]] if not total else list(idx[i]) + list(set(fc_idx[j])-set(idx[i]))

# def get_four_beh(fc_idx, corr_f, corr_m, fc_f, fc_m):
#     cf, cm, ff, fm = corr_f[fc_idx], corr_m[fc_idx], fc_f[fc_idx], fc_m[fc_idx]
#     f, m = four_behaviors(fc_idx, cf, ff), four_behaviors(fc_idx, cm, fm)
#     return f, m

# #### Fig. 2
# def acc_all_fc(accs, main_f, main_m, ind_f, ind_m, file_name):
#     """accs: classification accuracy matrix of female and male \n
#     main_f: classification accuracy of female on main data \n
#     ind_f: classification accuracy of female on independent data."""

#     fig, cs = plt.figure(figsize=(9,9)), ['peru', 'gray']
#     gs = Grids(3, 4, figure=fig, hspace=0.2, wspace=1.2)

#     xlabel, xtick = 'Age range', ['49-52','53-56','57-60','61-64','65-68','69-72','73-76']
#     titles = ['a. Classification accuracy (%)\nin females', 'b. Classification accuracy (%)\nin males', 'c. Mean accuracy of similar classification tasks']
#     axes = fig.add_subplot(gs[:2,:2]), fig.add_subplot(gs[:2,2:])
#     [heatmap(fig, ax, acc, 95, 50, t, xlabel, xlabel, xtick, xtick, 45, 11, 'rainbow', 9) \
#         for ax, acc, t in zip(axes, accs, titles)]

#     xlabel, ylabel = 'Age difference', 'Classification\naccuracy (%)'
#     ax = fig.add_subplot(gs[2,:3])
#     hatch, label = [[None]*2, ['////']*2], [[' '*3]*2, ['Main data', 'Independent data']]
#     acc_bar(ax, [main_f, ind_f], [main_m, ind_m], 0.5, xlabel, ylabel, hatch, label, titles[-1], cs)
#     plt.tight_layout(), plt.savefig(file_name+'.pdf'), plt.savefig(file_name+'.tif', dpi=500)

# #### Fig. 3
# def acc_dif_feat(main_f, main_m, ind_f, ind_m, ave_acc, effc, file_name):
#     """main_f: classification accuracy of female on main data (using different features)\n 
#     ind_f: classification accuracy of female on main data (using different features)\n 
#     ave_acc: overall classification accuracy \n
#     effc: efficiency matrix. """

#     fig = plt.figure(figsize=(12,10.5))
#     gs = Grids(2, 3, figure=fig, hspace=0.5, wspace=0.6)
#     xlabel, ylabel = 'Age difference', 'Classification accuracy (%)'
#     hatch, label = [[None]*6, ['////']*6], [[' '*3]*6, ['Gender-common FC', 'Female-specific FC', 'Male-specific FC', 'Gender-common & female-specific FC', 'Gender-common & male-specific FC', 'All FC']]
#     titles = ['a. Mean accuracy of similar classification tasks\non main data', 'b. Mean accuracy of similar classification tasks\non independent data']
#     cs = ['yellow','orange','deepskyblue','hotpink', 'limegreen']
#     ax0, ax1 = fig.add_subplot(gs[0,:2]), fig.add_subplot(gs[1,:2])
#     acc_bar(ax0, main_f, main_m, 0.25, xlabel, ylabel, hatch, label, titles[0], cs+['peru']) 
#     acc_bar(ax1, ind_f, ind_m, 0.25, xlabel, ylabel, hatch, label, titles[1], cs+['gray'])

#     ax2, ax3 = fig.add_subplot(gs[0,2]), fig.add_subplot(gs[1,2])
#     titles = ['c. Overall accuracy (%)', 'd. Efficiency matrix']
#     xtick = ['Main data\n(Female)', 'Independent data\n(Female)', 'Main data\n(Male)', 'Independent data\n(Male)']
#     ytick = ['Gender-common FC', 'Female-specific FC', 'Male-specific FC', 'Gender-common &\nfemale-specific FC', 'Gender-common &\nmale-specific FC', 'All FC']
#     heatmap(fig, ax2, ave_acc, 70, 56, titles[0], None, None, xtick, ytick, 45, 12, 'rainbow', 9)
#     heatmap(fig, ax3, effc, 1, 0.84, titles[1], None, None, xtick, ytick, 45, 12, 'rainbow', 9)
#     plt.tight_layout(), plt.savefig(file_name+'.pdf'), plt.savefig(file_name+'.tif', dpi=500)

# #### Fig. 4
# def corr_distribution(i012, corr_f, corr_m, fc_f, fc_m, file_name):
#     fig, colors = plt.figure(figsize=(10.5,10)), ['dodgerblue','coral','fuchsia','lime']
#     gs = Grids(2, 2, figure=fig) # replace with subplots
#     axes = fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 1])

#     loc, leg = [(0.37, 0.0), (-0.3, 0.0), (0.37, 0.33), (-0.3, 0.33), (-0.3, 0.67)], []
#     leg_titles = ['Paired t-test (female-specific FC)', 'Paired t-test (male-specific FC)', 'Paired t-test (gender-common FC)', 'Male  Female  FC  corr']
#     for j, (fc_idx, ax) in enumerate(zip(i012, axes)):
#         beh_f, beh_m = get_four_beh(fc_idx, corr_f, corr_m, fc_f, fc_m)
#         h0, l0, l1 = beh_sactter(ax, j, corr_f, corr_m, beh_f, beh_m, colors)
#         print(h0, l0, '$$$$$$$$$$$$$$$')
#         if j == 2:
#             leg.append(axes[-1].legend(h0[0], l1[0], handletextpad=0, title=leg_titles[j], ncol=2, columnspacing=0.02, loc=loc[j], fontsize=12, title_fontsize=12))
#             leg.append(axes[-1].legend(h0[1], l1[1], handletextpad=0, title=leg_titles[j], ncol=2, columnspacing=0.02, loc=loc[j+1], fontsize=12, title_fontsize=12))
#         else:
#             leg.append(axes[-1].legend(h0, l1, handletextpad=0, title=leg_titles[j], ncol=2, columnspacing=0.02, loc=loc[j], fontsize=12, title_fontsize=12))
#     leg.append(axes[-1].legend(h0[-1], l0, handletextpad=0, title=leg_titles[-1], ncol=2, columnspacing=0.02, loc=loc[-1], fontsize=12, title_fontsize=12))
#     [axes[-1].add_artist(lg) for lg in leg[:-1]], axes[-1].axis('off')
#     plt.tight_layout(), plt.savefig(file_name+'.pdf'), plt.savefig(file_name+'.tif', dpi=500)

# #### Fig. 5
# def fc_change_pattern(i012, corr_f, corr_m, fc_f, fc_m, file_name):
#     beh = [get_four_beh(idx, corr_f, corr_m, fc_f[0], fc_m[0])[i%2] for i,idx in enumerate(i012)]
#     fig = plt.figure(constrained_layout=True, figsize=(14.4,12))
#     gs, titles = Grids(3, 4, figure=fig), ['a. Stable gender-common FC', 'b. Stable female-specific FC', 'c. Stable male-specific FC']
#     ax_g = fig.add_subplot(gs[:,:])
#     ax_g.axis('off')
#     for i in range(3):
#         ax = fig.add_subplot(gs[i,:])
#         ax.axis("off"), ax.set_title(titles[i], weight='bold', y=1.09)
#     xlabel, ylabel, colors = 'FC strength in males', 'FC strength in females', plt.get_cmap('rainbow', 28)
#     ls = ['FC: '+r'$+$'+r', corr: $ -$', 'FC: '+r'$-$'+r', corr: $ -$', 'FC: '+r'$+$'+r', corr: $ +$','FC: '+r'$-$'+r', corr: $ +$']

#     for i, idxs in enumerate([beh[2],beh[0],beh[1]]): # 3 type FCs
#         for j in range(4): # 4 behaviors
#             vv, ax = [], fig.add_subplot(gs[i,j])
#             ax.set_title(ls[j], weight='bold', fontsize=14), ax.set_xlabel(xlabel, weight='bold'), ax.set_ylabel(ylabel, weight='bold')
#             for k in range(28):
#                 _, v = ellipse(fc_m[k][idxs[j]], fc_f[k][idxs[j]], ax, n_std=0.1, facecolor=colors(k), alpha=0.5, label=49+k)
#                 vv.append(v)
#             vv = np.array(vv)
#             xl, xr, yl, yr = vv[:,0].min(), vv[:,1].max(), vv[:,2].min(), vv[:,3].max()
#             l,r = min(xl, yl)-0.02, max(xr, yr)+0.02
#             ax.set_xlim(l,r), ax.set_ylim(l,r)
#             # ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f')), ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#             ax.locator_params(axis='x', nbins=(r-l)//0.1+1), ax.locator_params(axis='y', nbins=(r-l)//0.1+1)
#             ax.add_patch(Rectangle((xl, yl), xr-xl, yr-yl, zorder=0, ec='black',fc='white', ls='--', lw=2.4))
#             ax.plot([l, r], [l, r], ls='--', zorder=0, color='black', lw=1)

#     h, l = ax.get_legend_handles_labels()
#     ax_g.legend(h, l, loc=(1.01,0.2), fontsize=12, title='Age', title_fontsize=14, handlelength=1)
#     plt.tight_layout(), plt.savefig(file_name+'.pdf'), plt.savefig(file_name+'.tif', dpi=500)

# #### Fig. 6
# def four_patterns_domain(fc_name, i012s, i012, cp012, m012, file_name, figsize, loc_):
#     def all_inf(i012, sex, fc_name, cp012, m012):
#         fc_idx, s = i012[sex], sex%2
#         dom = fcidx2dom(fc_idx, fc_name)
#         dif = cor_sim_dif(dom, cp012[0][:,0], cp012[1][:,0], sex)
#         beh_f = dom2behaviors(dom, cp012[s][:,0], m012[s][0])
#         dif_ = cor_sim_dif_(beh_f, cp012[0][:,0], cp012[1][:,0], sex)
#         beh_f_cot, beh_m_cot = behavior2idx(beh_f, cp012[1-s][:,0], m012[1-s][0]) # 以F为标准
#         return dom, dif, dif_, beh_f_cot, beh_m_cot
    
#     fig, ax = plt.subplots(3,2,figsize=figsize)
#     titles = ['b. Stable female-specific FC','c. Stable male-specific FC','a. Stable gender-common FC']
#     loc, ax = [0.01,0.44,0.01,0.72], ax[[1,2,0]]
#     loc = loc_
#     v300 = []
#     for j,i in enumerate(i012):
#         dom, sim, sim_, beh_f_cot, beh_m_cot = all_inf(i012, j, fc_name, cp012, m012)
#         inc_dec_fc_bar(ax[j,0], list(dom.keys()), beh_f_cot.values(), beh_m_cot.values(), 0.34, titles[j], len(i), loc, sim.values())
#         v300.append(sim_)

#     vs, vs_ = [defaultdict(list) for _ in range(3)], [defaultdict(list) for _ in range(3)]
#     for i012 in i012s:
#         for j,i in enumerate(i012):
#             dom, dif, dif_, _,_ = all_inf(i012, j, fc_name, cp012, m012)
#             for k in dif: vs[j][k].append(dif[k])
#             for k in dif_: vs_[j][k].append(dif_[k])
#     for it in vs:
#         for k in it: it[k] = [np.sum(it[k])/5]
#     for it in vs_:
#         for k in it: it[k] = [np.sum(it[k], axis=0)/5]
#     for it, it_ in zip(vs_, v300):
#         for k in it:
#             if k not in it_.keys(): it_[k] = [0,0,0,0]

#     cs = ['dodgerblue','coral','fuchsia','lime']
#     titles = ['e. Stable female-specific FC','f. Stable male-specific FC','d. Stable gender-common FC']
#     for ax_, it, it_, title in zip(ax[:,1], vs_, v300, titles):
#         ax_.set_title(title, weight='bold')
#         it, it_ = OrderedDict(sorted(it.items())), OrderedDict(sorted(it_.items()))
#         k, v = np.array(list(it.keys())), np.vstack(list(it.values()))
#         k_, v_ = np.array(list(it_.keys())), np.vstack(list(it_.values()))
#         assert (~(k_ == k)).sum() == 0
#         j, x = np.argsort(v.sum(axis=1)), np.arange(len(k))
#         # j = np.argsort(k)
#         j = np.arange(len(k))
#         dom_n, dom_v = k[np.argmax(v, axis=0)], v[np.argmax(v, axis=0), np.arange(4)]
#         dom_n_, dom_v_ = k_[np.argmax(v_, axis=0)], v_[np.argmax(v_, axis=0), np.arange(4)]
#         ax_.set_xticks(x), ax_.set_xticklabels(k[j], rotation=45,ha='right', rotation_mode="anchor")
        
#         # plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
#         for ii in range(4):
#             vp, vn = v*(v>=0), v*(v<0)
#             vp_, vn_ = v_*(v_>=0), v_*(v_<0)
#             if ii==0:
#                 ax_.bar(x+0.15, vp[:,0][j], width=0.3, color=cs[ii], label='{} {:.2f}'.format(dom_n[ii], dom_v[ii]),ec='black',hatch='....'), ax_.bar(x+0.15, vn[:,0][j], width=0.3, color=cs[ii],ec='black',hatch='....')
#                 ax_.bar(x-0.15, vp_[:,0][j], width=0.3, color=cs[ii], label='{} {:.2f}'.format(dom_n_[ii], dom_v_[ii]),ec='black'), ax_.bar(x-0.15, vn_[:,0][j], width=0.3, color=cs[ii],ec='black')
#             else:
#                 ax_.bar(x+0.15, vp[:,ii][j], bottom=vp[:,:ii].sum(axis=1)[j], width=0.3, color=cs[ii], label='{} {:.2f}'.format(dom_n[ii], dom_v[ii]),ec='black',hatch='....'), ax_.bar(x+0.15, vn[:,ii][j], bottom=vn[:,:ii].sum(axis=1)[j], width=0.3, color=cs[ii],ec='black',hatch='....')
#                 ax_.bar(x-0.15, vp_[:,ii][j], bottom=vp_[:,:ii].sum(axis=1)[j], width=0.3, color=cs[ii], label='{} {:.2f}'.format(dom_n_[ii], dom_v_[ii]),ec='black'), ax_.bar(x-0.15, vn_[:,ii][j], bottom=vn_[:,:ii].sum(axis=1)[j], width=0.3, color=cs[ii],ec='black')
#         h0, l0 = ax_.get_legend_handles_labels()
#         h00, h01, l00, l01 = [], [], [], []
#         for kk in range(8):
#             if kk%2 == 0: h00.append(h0[kk]), l00.append(l0[kk])
#             else: h01.append(h0[kk]), l01.append(l0[kk])
#         leg = ax_.legend(h01+h00, l01+l00, title=' '*12 +'n=300'+' '*11 + 'different n combined', fontsize=12, title_fontsize=12, ncol=2,columnspacing=0.24,loc='upper left')
#         leg._legend_box.align = "left"
#         ax_.add_artist(leg)
#         ax_.set_xlim([-1, len(x)])
#     ax[0,1].set_ylabel('Female specificity measure', weight='bold'), ax[1,1].set_ylabel('Male specificity measure', weight='bold'), ax[2,1].set_ylabel('Commonality measure', weight='bold')
#     plt.tight_layout(), plt.savefig(file_name+'.pdf'), plt.savefig(file_name+'.tif', dpi=500)

# #### Fig. 7
# def traj(uk100, i012, fc_name, corr_f, corr_m, fc_f, fc_m, std_f, std_m, file_name):
#     def pos_mask(nii):
#         aff = nii.affine
#         data = image.get_data(nii)
#         data = data * (data > 0)
#         img = image.new_img_like(nii, data, aff)
#         return img
#     mask = image.get_data(image.index_img(uk100, 1)) != 0
#     def nor_mask(nii):
#         aff = nii.affine
#         data = image.get_data(nii)
#         m,s = data[mask].mean(), data[mask].std()
#         data = (data-m)/s
#         data = data * (data > 0)
#         img = image.new_img_like(nii, data, aff)
#         return img
#     fig = plt.figure(figsize=(16,30))
#     _gs0 = Grids(3, 1, figure=fig, hspace=0.2)
#     titles = ['a. Stable gender-common FC', 'b. Stable female-specific FC', 'c. Stable male-specific FC']
#     coors = {j:'y' for j in range(100)}
#     coors[20], coors[22], coors[57], coors[60], coors[64] = 'x', 'x', 'z', 'z', 'z'
#     for i, fc_idx in enumerate(i012):
#         gs0 = grids.GridSpecFromSubplotSpec(2, 5, subplot_spec=_gs0[i], hspace=0.24, wspace=0.24)
#         ax = fig.add_subplot(gs0[:,:])
#         ax.set_title(titles[i], y=1.04, weight='bold'), ax.axis('off')
#         fc, cf,cm, ff,fm, sf, sm = fc_name[fc_idx], corr_f[fc_idx], corr_m[fc_idx], fc_f[:,fc_idx].T, fc_m[:,fc_idx].T, std_f[:,fc_idx].T, std_m[:,fc_idx].T

#         for j in range(len(fc_idx)):
#             gs = grids.GridSpecFromSubplotSpec(3, 2, subplot_spec=gs0[j//5, j%5], wspace=0.02)
#             ax, axes = fig.add_subplot(gs[1:3, :]), [fig.add_subplot(gs[0,k]) for k in range(2)]
#             b, t = fc[j].split('-'), 'F: {:.2f}, M: {:.2f}'.format(cf[j], cm[j])
#             for bb, _ax in zip(b, axes):
#                 nii = image.index_img(uk100, int(bb[4:-1])-1)
#                 a = plotting.plot_stat_map(image.smooth_img(nor_mask(nii), 6), threshold=3, display_mode=coors[int(bb.split('(')[1][:-1])], axes=_ax, annotate=False, colorbar=False, cut_coords=1, symmetric_cbar=False)
#                 a.title(bb, x=0.32, y=1.14, size=10, color='black', bgcolor='white', alpha=0)
#                 # a0 = plotting.plot_glass_brain(image.index_img(uk100, int(l[4:-1])-1), threshold=3, display_mode='y', plot_abs=False, axes=ax0, vmin=-20, vmax=30, annotate=False)
#                 # a1 = plotting.plot_glass_brain(image.index_img(uk100, int(r[4:-1])-1), threshold=3, display_mode='y', plot_abs=False, axes=ax1, vmin=-20, vmax=30, annotate=False)
#             ax.set_title(t, weight='bold', fontsize=12, y=0.97), ax.set_xlabel('Age', weight='bold'), (ax.set_ylabel('FC strength', weight='bold') if j%5==0 else None)
#             tendency(ax, np.arange(48,76), ff[j], sf[j], ['red','deeppink'], 'F')
#             tendency(ax, np.arange(48,76), fm[j], sm[j], ['tab:blue','deepskyblue'], 'M')
#             ax.locator_params(axis='x', nbins=6), ax.locator_params(axis='y', nbins=6), ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#     plt.tight_layout(), plt.savefig(file_name+'.pdf'), plt.savefig(file_name+'.tif', dpi=500)


# #### Fig 2,3
# def heatmap(fig, ax, mat, vmax, vmin, title, xlabel, ylabel, xtick, ytick, rotation, fontsize, cmap, nbins):
#     v, yy, xx = np.copy(mat), np.arange(mat.shape[0]), np.arange(mat.shape[1]) # row = y
#     v[v==0] = np.nan
#     im = ax.imshow(v, vmax=vmax, vmin=vmin, cmap=cmap)
#     ax.set_title(title,weight='bold',y=1.02),ax.set_xlabel(xlabel,weight='bold'),ax.set_ylabel(ylabel,weight='bold')
#     ax.set_xticks(xx), ax.set_xticklabels(xtick), ax.set_yticks(yy), ax.set_yticklabels(ytick)
#     [plt.setp(k, rotation=rotation, ha="right", rotation_mode="anchor") for k in [ax.get_xticklabels(), ax.get_yticklabels()]]
#     divider = make_axes_locatable(ax)
#     cax = divider.append_axes('right', size='4%', pad=0.1)
#     cb = fig.colorbar(im, cax=cax, orientation='vertical')
#     tick_locator = ticker.MaxNLocator(nbins=nbins)
#     cb.locator = tick_locator
#     cb.update_ticks()
#     [ax.text(x, y, '{:.2f}'.format(v[y,x]), ha="center", va="center", color="black", fontsize=fontsize)\
#         for x in xx for y in yy if not np.isnan(v[y,x])]
#     return im

# def acc_bar(ax, fv, mv, width, xlabel, ylabel, hatchs, labels, title, colors=None):
#     """input:, f, m: n_type_feat, n_acc"""
#     f_plt = lambda ax,x,y,w,h,l,c: ax.bar(x,y,width=w,ec='black',hatch=h,label=l,color=c, zorder=2)
#     if colors is None: colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
#     n, xtick, ytick = len(fv), np.arange(4,25,4), np.arange(50, 96, 5)
#     steps = -np.arange(0.5-n, n+0.5, 1).reshape(-1, 2)
#     ax.set_title(title, weight='bold'), ax.set_xlabel(xlabel, weight='bold'), ax.set_ylabel(ylabel, weight='bold')
#     ax.set_xlim([2, 26]), ax.set_ylim([50, 95]), ax.set_xticks(xtick),ax.set_xticklabels(xtick),ax.set_yticks(ytick),ax.set_yticklabels(ytick)
#     [ax.plot([2, 26], [k, k], ls=(0,(5,10)), zorder=0, color='gray', lw=0.4) for k in ytick[1:-1]]
#     for ss, vv, hh, ll in zip(steps.T, [mv,fv], hatchs, labels): [f_plt(ax, xtick-s*width, v, width, h, l, c) for s,v,h,l,c in zip(ss, vv, hh, ll, colors)]
#     leg = ax.legend(title='Male  Female', ncol=2, columnspacing=0.2, framealpha=1, loc='upper left',handlelength=1) # fontsize=12, title_fontsize=12
#     leg._legend_box.align = "left"

# #### Fig 4
# def beh_sactter(ax, sex, cor_f, cor_m, idxs_f, idxs_m, colors):
#     l_m, l_f = ['vs.']*4, [' '*8+r'$+\    \ -$', ' '*8+r'$-\    \ -$', ' '*8+r'$+\    \ +$', ' '*8+r'$-\    \ +$']
#     tp, title = [], 'b. Stable female-specific FC' if sex==0 else 'c. Stable male-specific FC' if sex==1 else 'a. Stable gender-common FC'
#     ax.set_title(title, weight='bold')
#     x, xlabel, ylabel = np.arange(-1, 1.1, 0.1), 'Correlation between FC strength and age\nin males', 'Correlation between FC strength and age\nin females'
#     ax.plot(x, x, c='black',ls='-', zorder=0), ax.set_ylim([-1, 1]), ax.set_xlim([-1, 1])
#     ax.vlines(0, -1, 1, ls='--', color='black', zorder=0), ax.hlines(0, -1, 1, ls='--', color='black', zorder=0)
#     ax.set_xlabel(xlabel, weight='bold'), ax.set_ylabel(ylabel, weight='bold')
#     for _sex, idxs in enumerate([idxs_f, idxs_m]): # right half first
#         _tp, l = [], [l_f, l_m][_sex]
#         h, mark = [None, semicircles[0]] if _sex==1 else ['//////', semicircles[1]]
#         for j,i in enumerate(idxs):
#             ax.scatter(cor_m[i], cor_f[i], label=l[j], c=colors[j], ec='black' ,s=100, zorder=2, marker=mark, hatch=h, alpha=0.8)
#             if _sex==sex%2: ax.scatter(cor_m[i].mean(), cor_f[i].mean(), c=colors[j],s=249, marker='x', linewidths=2.14, zorder=3)
#             _tp.append(list(ttest_rel(cor_m[i], cor_f[i]))) # m vs. f
#         if sex == 2: tp += _tp
#         else: 
#             if _sex == sex%2: tp = _tp
#         [ax.scatter(j,j, label=j, c='white', ec='black' ,s=100, zorder=2, marker=mark, hatch=h, alpha=0.8) for j in range(10,14)]
#     ## first legend
#     h, l = ax.get_legend_handles_labels()
#     if sex==0: h0 = h[12:] + h[:4]
#     elif sex==1: h0 = h[8:12]+h[4:8]
#     else: h0 = (h[12:] + h[:4], h[8:12]+h[4:8], h[8:12] + h[:4])

#     ## change legend
#     if sex == 2: 
#         l0, l1 = ['']*4+l[:4], [l_m+['T = {:.2f}, p = {:.2e}'.format(t,p) for t,p in tp[:4]], l_m+['T = {:.2f}, p = {:.2e}'.format(t,p) for t,p in tp[4:]]]
#     else:
#         l0, l1 = ['']*4+l[:4], l_m+['T = {:.2f}, p = {:.2e}'.format(t,p) for t,p in tp]
#     return h0,l0,l1

# #### Fig 6
# def inc_dec_fc_bar(ax, dom_name, n_female, n_male, width, title, n_fc, position, dif_v):
#     xs, w, cs = np.arange(len(dom_name)), width, ['dodgerblue','coral','fuchsia','lime'] #['tab:blue','tab:pink','tab:orange','deepskyblue']
#     b, ls = 0, [' '*9+r'$+\    \ -$', ' '*9+r'$-\    \ -$', ' '*9+r'$+\    \ +$', ' '*9+r'$-\    \ +$']

#     nf, nm = [], []
#     for x, vm, vf, d in zip(xs, n_male, n_female, dif_v):
#         b = 0
#         [[nf.append(np.isin(vf, j).sum()), nm.append(np.isin(vm, j).sum())] for j in range(4)]
#         for m,f in zip(vm, vf):
#             ax.bar(x-w/2, 1, width=w, ec='black', color=cs[m], bottom=b)
#             ax.bar(x+w/2, 1, width=w, ec='black', color=cs[f], bottom=b, hatch='////')
#             b += 1
#         # ax.text(x-w*1.5, b+0.04, '{:.2f}'.format(d), fontsize=10, rotation=24)
        
#     [ax.bar(x-w/2, 0, width=w, color=cs[j], ec='black', label='  ', bottom=0) for j in range(4)]
#     [ax.bar(x+w/2, 0, width=w, color=cs[j], ec='black', label=ls[j], bottom=0, hatch='////') for j in range(4)]

#     leg1 = ax.legend(title='Male  Female  FC  corr', ncol=2, columnspacing=0.66, handletextpad=0.18, handlelength=1.4, fontsize=12, title_fontsize=12) # 第一个标签
#     leg1._legend_box.align = "left"

#     nf, nm = np.array(nf).reshape(-1,4), np.array(nm).reshape(-1,4)
    
#     #### legend (percent)
#     in_i = [j for j,k in enumerate(dom_name) if k[:2]==k[-2:]] ## within idx
#     btn_i = [j for j,k in enumerate(dom_name) if k[:2]!=k[-2:]] ## between idx

#     f_n, m_n = nf.sum(axis=0), nm.sum(axis=0) #### total number
#     f_in, m_in = nf[in_i].sum(axis=0), nm[in_i].sum(axis=0) #### 个数
#     f_btn, m_btn = nf[btn_i].sum(axis=0), nm[btn_i].sum(axis=0) #### 个数
#     h0, l0 = ax.get_legend_handles_labels()
#     l0 = ['{:d} ({:d} | {:d})'.format(total, in_n, btn_n) for total, in_n, btn_n in\
#         zip(np.hstack([m_n, f_n]), np.hstack([m_in, f_in]),np.hstack([m_btn, f_btn]))]
#     leg2 = ax.legend(h0, l0, ncol=2, loc=(position[0], position[1]), columnspacing=0.18,\
#         title='FC number (within | between domains)', handletextpad=0.18, handlelength=1.4, fontsize=12, title_fontsize=12)

#     h1, l1 = ax.get_legend_handles_labels()
#     l1 = ['{:.1f}% ({:.1f}% | {:.1f}%)'.format(total*100/n_fc, in_n*100/n_fc, btn_n*100/n_fc) for total, in_n, btn_n in\
#         zip(np.hstack([m_n, f_n]), np.hstack([m_in, f_in]),np.hstack([m_btn, f_btn]))]
#     leg3 = ax.legend(h1, l1, ncol=2, loc=(position[2], position[3]), columnspacing=0.18,\
#         title='Percentage (within | between domains)', handletextpad=0.18, handlelength=1.4, fontsize=12, title_fontsize=12)
#     ax.add_artist(leg1), ax.add_artist(leg2)
    
#     # for j in range(len(dom_name)):
#     #     if dom_name[j][:2] == dom_name[j][-2:]: dom_name[j] = '*' + dom_name[j]
#     ax.set_xticks(xs), ax.set_xticklabels(dom_name), ax.set_title(title, weight='bold')
#     ax.set_yticks(np.arange(0,20,2)), ax.set_yticklabels(np.arange(0,20,2))
#     plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
#     ax.set_xlim([-1, len(dom_name)]), ax.set_ylabel('FC number', weight='bold')
#     plt.tight_layout()

# #### Fig 8 
# def cog_fc(pt, file_name, i012, m012, cp012, cp_f_fi, cp_f_nm, cp_f_rt, cp_m_fi, cp_m_nm, cp_m_rt):
#     def cogs_scatter(ax, fc_idx, cor_f, cor_m, m_f, m_m, fi_f, nm_f, rt_f, fi_m, nm_m, rt_m, sex, title):
#         beh_f, beh_m = get_four_beh(fc_idx, cor_f, cor_m, m_f, m_m)
#         m0, m1 = semicircles[0], semicircles[1]
#         cs = ['dodgerblue','coral','fuchsia','lime']
#         def sct(x, y, d, zs):
#             for j in range(4):
#                 ax.scatter(x[beh_m[j]], y[beh_m[j]], zdir=d, zs=zs, alpha=0.8, marker=m0, s=88, color=cs[j], ec='black', zorder=1)
#                 ax.scatter(x[beh_f[j]], y[beh_f[j]], zdir=d, zs=zs, alpha=0.8, marker=m1, s=88, color=cs[j], ec='black', hatch='//////', zorder=1)
#                 if sex==1: x_, y_ = x[beh_m[j]].mean(), y[beh_m[j]].mean()
#                 else: x_, y_ = x[beh_f[j]].mean(), y[beh_f[j]].mean()
#                 ax.scatter(x_, y_, zdir=d, zs=zs, marker='x',s=240, lw=2.4, color=cs[j], zorder=1000)
#         ax.plot(np.arange(-1,1.1,0.1), np.arange(-1,1.1,0.1),'k-', zdir='x', zs=-1, zorder=0),ax.plot(np.arange(-1,1.1,0.1), np.arange(-1,1.1,0.1),'k-', zdir='y', zs=1, zorder=0),ax.plot(np.arange(-1,1.1,0.1), np.arange(-1,1.1,0.1),'k-', zdir='z', zs=-1, zorder=0)
        
#         sct(fi_m, fi_f, 'x', -1), sct(nm_m, nm_f, 'y', 1), sct(rt_m, rt_f, 'z', -1)
#         ax.set_xlim([-1, 1]), ax.set_ylim([-1, 1]), ax.set_zlim([-1, 1]), ax.grid(False)

#         ax.text(0.02, 1, 0.9, 'rF', zdir='x', fontsize=14),ax.text(0.9, 1, -0.2, 'rM', zdir='x', fontsize=14)
#         a_ = Arrow3D([-1, 1], [1, 1], [0, 0], mutation_scale=20, lw=1.5,ls='-', arrowstyle="->", color="black")
#         b_ = Arrow3D([0, 0], [1, 1], [-1, 1], mutation_scale=20, lw=1.5,ls='-', arrowstyle="->", color="black")
#         ax.add_artist(a_), ax.add_artist(b_), ax.text(-0.75, 1, 0.75, 'NM', fontsize=16, color='blue')

#         ax.text(-0.18, 0.94, -1.1, 'rF', zdir='x', fontsize=14), ax.text(0.95, -0.22, -1, 'rM', zdir='x', fontsize=14)
#         a_ = Arrow3D([-1, 1], [0, 0], [-1, -1], mutation_scale=20, lw=1.5,ls='-', arrowstyle="->", color="black")
#         b_ = Arrow3D([0, 0], [-1, 1], [-1, -1], mutation_scale=20, lw=1.5,ls='-', arrowstyle="->", color="black")
#         ax.add_artist(a_), ax.add_artist(b_), ax.text(-0.75, 0.5, -1, 'RT', fontsize=16, color='blue')

#         ax.text(-1, 0.02, 0.9, 'rF', zdir='y', fontsize=14),ax.text(-1, 0.76, -0.15, 'rM', zdir='y', fontsize=14)
#         a_ = Arrow3D([-1,-1], [-1,1], [0,0], mutation_scale=20, lw=1.5,ls='-', arrowstyle="->", color="black")
#         b_ = Arrow3D([-1,-1], [0,0], [-1,1], mutation_scale=20, lw=1.5,ls='-', arrowstyle="->", color="black")
#         ax.add_artist(a_), ax.add_artist(b_), ax.text(-1, -0.75, 0.75, 'FI', fontsize=16, color='blue')

#         ax.set_title(title, y=0.98, weight='bold')

#     fig = plt.figure(figsize=(14,14))
#     gs = Grids(nrows=2, ncols=2)

#     # ax = fig.add_subplot(222, projection='3d')
#     ax = fig.add_subplot(gs[0, 1], projection='3d')
#     cogs_scatter(ax, i012[0], cp012[0][:,0], cp012[1][:,0], m012[0][0], m012[1][0],\
#         cp_f_fi, cp_f_nm, cp_f_rt, cp_m_fi, cp_m_nm, cp_m_rt, 0, 'b. Stable female-specific FC')

#     # ax = fig.add_subplot(223, projection='3d')
#     ax = fig.add_subplot(gs[1, 0], projection='3d')
#     cogs_scatter(ax, i012[1], cp012[0][:,0], cp012[1][:,0], m012[0][0], m012[1][0],\
#         cp_f_fi, cp_f_nm, cp_f_rt, cp_m_fi, cp_m_nm, cp_m_rt, 1, 'c. Stable male-specific FC')

#     # ax = fig.add_subplot(221, projection='3d')
#     ax = fig.add_subplot(gs[0, 0], projection='3d')
#     cogs_scatter(ax, i012[2], cp012[0][:,0], cp012[1][:,0], m012[0][0], m012[1][0],\
#         cp_f_fi, cp_f_nm, cp_f_rt, cp_m_fi, cp_m_nm, cp_m_rt, 0, 'a. Stable gender-common FC')
    
#     fi_f = np.loadtxt(f'{pt}/fc_corrs/fi_f.txt')
#     fi_m = np.loadtxt(f'{pt}/fc_corrs/fi_m.txt')
#     nm_f = np.loadtxt(f'{pt}/fc_corrs/nm_f.txt')
#     nm_m = np.loadtxt(f'{pt}/fc_corrs/nm_m.txt')
#     rt_f = np.loadtxt(f'{pt}/fc_corrs/rt_f.txt')
#     rt_m = np.loadtxt(f'{pt}/fc_corrs/rt_m.txt')
#     fi_f_ = np.loadtxt(f'{pt}/fc_corrs/fi_f_std.txt')
#     fi_m_ = np.loadtxt(f'{pt}/fc_corrs/fi_m_std.txt')
#     nm_f_ = np.loadtxt(f'{pt}/fc_corrs/nm_f_std.txt')
#     nm_m_ = np.loadtxt(f'{pt}/fc_corrs/nm_m_std.txt')
#     rt_f_ = np.loadtxt(f'{pt}/fc_corrs/rt_f_std.txt')
#     rt_m_ = np.loadtxt(f'{pt}/fc_corrs/rt_m_std.txt')

#     plt.rcParams.update({'axes.titlesize':'20', 'axes.labelsize':'16',\
#         'xtick.labelsize': '14', 'ytick.labelsize': '14', "font.weight": "bold"})
#     c0, c1, x = ['red','deeppink'], ['tab:blue','deepskyblue'], np.arange(49,77)
#     ax = fig.add_subplot(gs[1, 1])
#     ax.set_title('d. Cognitive measures', y=0.9, weight='bold'), ax.axis('off')
#     gs0 = grids.GridSpecFromSubplotSpec(8, 14, subplot_spec=gs[1,1], hspace=0.1)
#     ax = fig.add_subplot(gs0[1:3, 2:-1])
#     ks = (np.polyfit(np.arange(28), fi_f, deg=1)[0], np.polyfit(np.arange(28), fi_m, deg=1)[0])
#     tendency(ax, x, fi_f, fi_f_, c0, 'Female'), tendency(ax, x, fi_m, fi_m_, c1, 'Male')
#     ax.set_title('F: {:.3f}, M: {:.3f}'.format(*ks),x=0.4, y=0.14, weight='bold', fontsize=16),ax.set_ylabel('FI', weight='bold')
#     ax.legend(loc=(0.8,1.04), framealpha=1, fontsize=11.4)
#     # axes[-1].legend(h0, l1, handletextpad=0, title=leg_titles[j], ncol=2, columnspacing=0.02, loc=loc[j], fontsize=12, title_fontsize=12))
#     # ax.plot(np.arange(49,77), fi_m, color='tab:blue'), ax.plot(np.arange(49,77), fi_f, color='red'),
#     ax = fig.add_subplot(gs0[3:5, 2:-1])
#     ks = (np.polyfit(np.arange(28), nm_f, deg=1)[0], np.polyfit(np.arange(28), nm_m, deg=1)[0])
#     tendency(ax, x, nm_m, nm_m_, c1, 'Male'), tendency(ax, x, nm_f, nm_f_, c0, 'Female')
#     ax.set_title('F: {:.3f}, M: {:.3f}'.format(*ks),x=0.4, y=0.12, weight='bold', fontsize=16),ax.set_ylabel('NM', weight='bold')
#     # ax.plot(np.arange(49,77), nm_m, color='tab:blue'), ax.plot(np.arange(49,77), nm_f, color='red'), 
#     ax = fig.add_subplot(gs0[5:7, 2:-1])
#     ks = (np.polyfit(np.arange(28), rt_f, deg=1)[0], np.polyfit(np.arange(28), rt_m, deg=1)[0])
#     tendency(ax, x, rt_m, rt_m_, c1, 'Male'), tendency(ax, x, rt_f, rt_f_, c0, 'Female')
#     ax.set_title('F: {:.3f}, M: {:.3f}'.format(*ks),x=0.4, y=0.7, weight='bold', fontsize=16),ax.set_ylabel('RT', weight='bold')
#     # ax.plot(np.arange(49,77), rt_m, color='tab:blue'), ax.plot(np.arange(49,77), rt_f, color='red'), 
#     ax.set_xlabel('Age', weight='bold')

#     plt.tight_layout(), plt.savefig(f'{file_name}.pdf'), plt.savefig(f'{file_name}.tif', dpi=500), plt.show()

# def uk_annotation(nii_path, net):
#     fig, _axes = plt.subplots(14, 4, figsize=(9*4-3, 14*3-9))
#     axes = _axes.flatten()
#     axes[-1].remove()
#     count = 0
#     def pos_mask(nii):
#         aff = nii.affine
#         data = image.get_data(nii)
#         data = data * (data > 0)
#         img = image.new_img_like(nii, data, aff)
#         return img
#     mask = image.get_data(image.index_img(nii_path, 1)) != 0
#     def nor_mask(nii):
#         aff = nii.affine
#         data = image.get_data(nii)
#         m,s = data[mask].mean(), data[mask].std()
#         data = (data-m)/s
#         data = data * (data > 0)
#         img = image.new_img_like(nii, data, aff)
#         return img
#     for k in net:
#         i = net[k]
#         for ii in i:
#             nii = image.index_img(nii_path, ii-1)
#             img = image.smooth_img(nor_mask(nii), 6)
#             a0 = plotting.plot_stat_map(img, threshold=3, axes=axes[count])
#             a0.title(f'IC{ii}:{k}',x=0.5, y=1.09, size=14, color='black', bgcolor='white', alpha=0)
#             count += 1
#     plt.savefig('FigS1_55good_compnts.pdf'), plt.savefig('FigS1_55good_compnts.tif', dpi=500)

# def fc_change(fc_idx, corr_f, corr_m, fc_f, fc_m, sex):
#     idxs = four_behaviors(fc_idx, corr_f[fc_idx], fc_f[0][fc_idx]) if sex==0 or sex==2 else four_behaviors(fc_idx, corr_m[fc_idx], fc_m[0][fc_idx])
#     pat = []
#     for i in idxs:
#         v = []
#         for x,y in zip(fc_f, fc_m):
#             x_m, y_m = x[i].mean(), y[i].mean()
#             var = np.cov(x[i], y[i])
#             # v.append([f'{x_m} ({var[0,0]})', f'{y_m} ({var[1,1]})', f'{var[0,1]}'])
#             v.append(['{:.2f} ({:.2f})'.format(x_m,var[0,0]), '{:.2f} ({:.2f})'.format(y_m,var[1,1]), '{:.2f}'.format(var[0,1])])
#         pat.append(v)
#     return np.hstack(pat)

# def fc_inf(fc_idx, fc_name, cp012, m012, sex):
#     def pattern_name(fc, corr):
#         name = np.zeros(len(fc), dtype='<U3')
#         name[(fc>0) & (corr>0)], name[(fc>0) & (corr<0)] = '++', '+-'
#         name[(fc<0) & (corr>0)], name[(fc<0) & (corr<0)] = '-+', '--'
#         return name
#     idx = select_fc(fc_idx, cp012[0][:,0], cp012[1][:,0], sex, total=True) # sort
#     fc_f, fc_m = m012[0][0][idx], m012[1][0][idx]
#     corr_f, corr_m = cp012[0][:,0][idx], cp012[1][:,0][idx]
#     patt_f, patt_m  = pattern_name(fc_f, corr_f), pattern_name(fc_m, corr_m)
#     return np.vstack([idx, fc_name[idx], fc_f, fc_m, corr_f, corr_m, patt_f, patt_m]).T