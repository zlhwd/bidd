# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import Http404
from math import ceil
from conf import labels_order, ordered_labels, page_size, syn_num, mongo_mols, mongo_fams, mongo_vars 
from utils import _id2id, make_link, make_pie_json

def index(req):
    visit_count = mongo_vars.find_one_and_update({'_id':'cfam_home_visit_count'},{'$inc':{'value':1}},upsert=True,return_document=True)['value']
    return render(req,'cfam/index.html', {'visit_count': visit_count})

def mols(req):
    selected_labels = req.GET.getlist('category')
    condition = {}
    if selected_labels:
        condition = {'label':{'$in':selected_labels}}
    all_mols_num = mongo_mols.count(condition)
    max_page = int(ceil(1.0*all_mols_num/page_size))

    page = req.GET.get('page')
    page = int(page) if page else 1
    if page < 1:
        page = 1
    elif page > max_page:
        page = max_page

    mols = list(mongo_mols.find(condition,['name','label','fam_id']).skip((page-1)*page_size).limit(page_size))
    map(_id2id,mols)

    return render(req,'cfam/mols.html',{
        'labels':ordered_labels,
        'selected_labels': selected_labels,
        'page':page,
        'max_page':max_page,
        'all_mols_num':all_mols_num,
        'mols':mols,
    })

def mol(req,mol_id):
    db_mol = mongo_mols.find_one({'_id':mol_id},{'fp':0})
    if not db_mol:
        raise Http404('Molecule %s does not exist!' % mol_id)
    _id2id(db_mol)
    for src_mol in db_mol['mols']:
        if 'synonyms' in src_mol:
            synonyms = []
            count = 0
            for syn in sorted(src_mol['synonyms'],key=len):
                if count % syn_num == 0:
                    synonyms.append((count+1,[]))
                synonyms[count/syn_num][1].append(syn)
                count += 1
            src_mol['synonyms'] = synonyms
        src_mol['link'] = make_link(src_mol['src'],src_mol['src_id'])

    return render(req,'cfam/mol.html',db_mol)

def fams(req):
    selected_labels = req.GET.getlist('category')
    condition = {}
    if selected_labels:
        condition = {'label':{'$in':selected_labels}}
    all_fams_num = mongo_fams.count(condition)
    max_page = int(ceil(1.0*all_fams_num/page_size))

    page = req.GET.get('page')
    page = int(page) if page else 1
    if page < 1:
        page = 1
    elif page > max_page:
        page = max_page

    fams = list(mongo_fams.find(condition,['name','label','seeds','members']).skip((page-1)*page_size).limit(page_size))
    map(_id2id,fams)

    return render(req,'cfam/fams.html',{
        'labels':ordered_labels,
        'selected_labels': selected_labels,
        'page':page,
        'max_page':max_page,
        'all_fams_num':all_fams_num,
        'fams':fams,
    })

def fam(req,fam_id):
    db_fam = mongo_fams.find_one({'_id':fam_id},['label','seeds','members'])
    if not db_fam:
        raise Http404('Family %s does not exist!' % fam_id)
    _id2id(db_fam)
    seeds = list(mongo_mols.find({'_id':{'$in':db_fam.pop('seeds')}},['name','label']))
    map(_id2id,seeds)
    db_fam['seeds'] = sorted(seeds,key=lambda x:labels_order[x['label']])
    db_fam['pie_json'] = make_pie_json(db_fam['seeds'])
    if 'members' in db_fam:
        members = list(mongo_mols.find({'_id':{'$in':db_fam.pop('members')}},['name','label']))
        map(_id2id,members)
        db_fam['members'] = sorted(members,key=lambda x:labels_order[x['label']])

    return render(req,'cfam/fam.html',db_fam)
